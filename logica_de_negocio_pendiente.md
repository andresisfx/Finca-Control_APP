# Análisis de User Stories (Arquitectura Offline-First)

Al tener un enfoque **Offline-First**, la regla de oro es: **El frontend (app móvil/web local) debe hacer la mayoría de los cálculos pesados y de visualización utilizando su base de datos local (ej. SQLite, WatermelonDB)**. El backend actúa principalmente como un **Motor de Sincronización (Sync)**, guardando la "fuente de la verdad" y resolviendo conflictos.

A continuación, el análisis de tus historias de usuario y cómo las hemos cubierto.

## 🟢 1. Historias ya cubiertas (CRUD Básico)
Estas historias ya están programadas en nuestro backend. El frontend simplemente enviará los datos cuando tenga internet para respaldarlos en PostgreSQL.

| User Story | Estado | Endpoint Backend Listo |
| :--- | :--- | :--- |
| Crear una finca | ✅ Listo | `POST /api/v1/fincas/` |
| Registrar un evento | ✅ Listo | `POST /api/v1/eventos/` |
| Agregar foto a animal | ✅ Listo | El campo `foto_url` está en el schema. El front sube la foto a S3/Firebase y manda la URL al backend. |
| Crear vendedores | ✅ Listo | `POST /api/v1/vendedores/` |
| Registrar venta de leche (producción) | ✅ Listo | `POST /api/v1/produccion/` |
| Crear una quincena | ✅ Listo | `POST /api/v1/quincenas/` |
| Crear un comprador | ✅ Listo | `POST /api/v1/compradores/` |
| Registrar entrega a comprador | ✅ Listo | `POST /api/v1/entregas/` |
| Añadir precio a quincena | ✅ Listo | `POST /api/v1/precios/` |

---

## 🟡 2. Historias de Cálculos e Historiales (Decisión de Diseño)
Aquí entran las historias de "ver historiales" y "ver totales". 
Como tu app es offline, **estos cálculos deben vivir en el Frontend**. Cuando el granjero esté sin internet, su teléfono debe sumar los litros de la base de datos local y multiplicarlos por el precio localmente para mostrarle el total en pantalla.

| User Story | ¿Dónde se calcula? | Acción requerida en Backend |
| :--- | :--- | :--- |
| Ver historial de un animal | Frontend + Backend | ✅ Ya tenemos `GET /eventos/animal/{id}` |
| Historial de ventas por vendedor por quincena | Frontend | ❌ Falta crear un endpoint en el backend que filtre la producción recibiendo fechas de inicio y fin. |
| Total litros vendedor/quincena | **Frontend** | El backend no necesita un endpoint para esto si el front ya sincroniza las producciones individuales. Sin embargo, para un dashboard Web (siempre online) sería útil tenerlo. |
| Total dinero adeudado vendedor | **Frontend** | (Litros * `precio_compra`). Se calcula en el teléfono. |
| Historial quincena por comprador | Frontend | ❌ Falta endpoint para filtrar entregas de un comprador por una quincena específica. |
| Total litros/dinero comprador | **Frontend** | Igual que con el vendedor, el cálculo financiero vive en el celular para estar siempre disponible. |

---

## 🔴 3. Historias Críticas Faltantes en el Backend
Estas son las piezas que nos faltan programar para completar la visión del proyecto:

1. **"Como usuario quiero iniciar sesión para acceder a mis datos"**
   * **Falta:** Hashing de contraseñas (para que no se guarden en texto plano).
   * **Falta:** Endpoint de Login que genere un Token JWT.
   * **Falta:** Proteger todos los endpoints actuales para que exijan el Token JWT y solo devuelvan datos del usuario autenticado.

2. **"Sistema de Sincronización (Offline to Online)"**
   * **Falta:** En el futuro necesitaremos endpoints de sincronización masiva (ej. `POST /api/v1/sync`) donde la app móvil mande un bloque grande de datos (50 animales, 20 eventos creados offline) para que el backend los inserte de golpe, en lugar de hacer 70 peticiones separadas.
