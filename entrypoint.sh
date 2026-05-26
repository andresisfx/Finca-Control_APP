#!/bin/bash
# entrypoint.sh — Espera a PostgreSQL, aplica migraciones y lanza uvicorn
# Se ejecuta como el usuario appuser (no-root) dentro del contenedor.

set -euo pipefail

# ──────────────────────────────────────────────────────────────
# 1. Esperar a que PostgreSQL esté listo
# ──────────────────────────────────────────────────────────────
# Se extrae el host y el puerto desde DATABASE_URL para no duplicar
# la configuración en variables separadas.
# Formato esperado: postgresql://user:pass@host:port/dbname

DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|.*@([^:/]+).*|\1|')
DB_PORT=$(echo "$DATABASE_URL" | sed -E 's|.*:([0-9]+)/.*|\1|')
DB_PORT="${DB_PORT:-5432}"

echo "[entrypoint] Esperando a PostgreSQL en ${DB_HOST}:${DB_PORT}..."

MAX_RETRIES=30
RETRY_INTERVAL=2
retries=0

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
    retries=$((retries + 1))
    if [ "$retries" -ge "$MAX_RETRIES" ]; then
        echo "[entrypoint] ERROR: PostgreSQL no respondio despues de $((MAX_RETRIES * RETRY_INTERVAL))s. Abortando."
        exit 1
    fi
    echo "[entrypoint] PostgreSQL no disponible aun, reintentando en ${RETRY_INTERVAL}s... (intento ${retries}/${MAX_RETRIES})"
    sleep "$RETRY_INTERVAL"
done

echo "[entrypoint] PostgreSQL disponible."

# ──────────────────────────────────────────────────────────────
# 2. Aplicar migraciones con Alembic
# ──────────────────────────────────────────────────────────────
echo "[entrypoint] Ejecutando migraciones: alembic upgrade head..."
alembic upgrade head
echo "[entrypoint] Migraciones aplicadas correctamente."

# ──────────────────────────────────────────────────────────────
# 3. Lanzar el proceso principal (uvicorn)
# Se usa exec para reemplazar el proceso bash por uvicorn,
# lo que permite que las señales del SO (SIGTERM, etc.) lleguen
# directamente a uvicorn en lugar de perderse en el shell.
# ──────────────────────────────────────────────────────────────
echo "[entrypoint] Iniciando servidor uvicorn..."
exec "$@"
