# FastAPI migration (Inferno Colombia)

Este directorio contiene la migración del ecommerce PHP a **Python + FastAPI**, reutilizando assets (`/css`, `/js`, `/img`, `/fonts`) y MySQL `threaderz_store`.

Ahora incluye **checkout asíncrono** con:
- **RabbitMQ**: encola solicitudes de pedido.
- **Redis**: guarda estado de procesamiento (`PENDING`, `CONFIRMED`, `FAILED`).

## Requisitos

- Python 3.10+
- MySQL (XAMPP)
- Docker Desktop (para Redis + RabbitMQ)
- Base de datos importada desde `store.sql`

## Configuración

1. Copia `.env.example` a `.env`.
2. Ajusta credenciales de MySQL y, si cambias puertos/hosts, también Redis y RabbitMQ.

## Instalación

```bash
recordar activar el xampp
primero deactivate el entorno que se ejecuta por defecto
cd fastapi_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Levantar Redis + RabbitMQ (Docker)

```bash
cd fastapi_app
docker compose up -d
```

- RabbitMQ Management: http://localhost:15672
- Usuario/clave por defecto: `guest` / `guest`

## Ejecutar API y Worker

En una terminal:

```bash
cd fastapi_app
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

En otra terminal:

```bash
primero deactivate el entorno que se ejecuta por defecto
cd fastapi_app
python -m app.worker
```

## Flujo de checkout asíncrono

1. Usuario hace clic en `Realizar Pedido` (`/checkout?place=1`).
2. API publica mensaje en RabbitMQ (cola `orders.create`) y guarda estado `PENDING` en Redis.
3. API redirige a `/checkout?request_id=<uuid>`.
4. Front consulta `/checkout/status/{request_id}` periódicamente.
5. Worker consume mensaje, crea orden en MySQL, limpia carrito y marca `CONFIRMED` (o `FAILED`) en Redis.

## Endpoints nuevos

- `GET /checkout/status/{request_id}`: devuelve estado JSON del pedido asíncrono.

## Rutas principales

- `/` Inicio
- `/shop` Tienda
- `/product/{product_id}` Detalle
- `/cart` Carrito
- `/checkout` Checkout
- `/login`, `/register`, `/logout`
- `/account?orders=1` y `/account?details=1`
- `/contact`
- `/admin/insert-product`
- `/productos`, `/productos/{id}` API catálogo

## Notas

- Autenticación por cookie de sesión (`customer_email`).
- Contraseñas siguen como en el proyecto original (texto plano en DB).
- Si RabbitMQ o Redis no están disponibles, el checkout asíncrono no podrá completarse.
