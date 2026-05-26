# ============================================================
# STAGE 1 — builder: instala dependencias en un virtualenv
# ============================================================
FROM python:3.11-slim AS builder

# Dependencias del sistema necesarias para compilar psycopg2-binary
# y cualquier extensión C de las dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Crear y activar virtualenv en una ruta predecible
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar solo requirements primero para aprovechar la cache de capas
COPY requirements.txt .

# Instalar sin cache de pip para mantener la imagen pequeña.
# Se filtran paquetes de testing (pytest, httpx) que no tienen lugar en producción.
# grep -v excluye líneas que empiecen por los paquetes de dev antes de pasarlas a pip.
RUN pip install --no-cache-dir --upgrade pip \
    && grep -vE "^(pytest|httpx)==" requirements.txt \
       | pip install --no-cache-dir -r /dev/stdin

# ============================================================
# STAGE 2 — runtime: imagen final mínima
# ============================================================
FROM python:3.11-slim AS runtime

# Librería de cliente PostgreSQL en tiempo de ejecución (no el compilador).
# postgresql-client es necesario para que entrypoint.sh pueda invocar pg_isready.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el virtualenv compilado desde el builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Usuario no-root por seguridad en producción
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

# Copiar el código de la aplicación
# El .dockerignore excluye .env, __pycache__, tests/, etc.
COPY --chown=appuser:appgroup . .

# Asegurar que el entrypoint sea ejecutable
RUN chmod +x /app/entrypoint.sh

# Cambiar al usuario no-root antes de exponer puertos y definir CMD
USER appuser

EXPOSE 8000

# Variables de entorno con valores seguros por defecto para producción.
# Estas son SOBREESCRITAS por docker-compose o por el orquestador.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False

# HEALTHCHECK: apunta al endpoint root definido en main.py
# Se espera 40 s antes del primer check para dar tiempo al entrypoint (migraciones)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# El entrypoint espera a la DB, ejecuta migraciones y luego lanza uvicorn.
# El módulo es "main:app" porque main.py está en el WORKDIR /app
# y la variable `app` es la instancia FastAPI.
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
