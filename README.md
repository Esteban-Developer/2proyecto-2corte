#  Inferno Colombia — E-commerce Distribuido (Corte 2)

<p align="center">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img alt="Redis" src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
  <img alt="RabbitMQ" src="https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

<p align="center">
  <b>Migración de e-commerce PHP a arquitectura distribuida con FastAPI + Redis + RabbitMQ</b>
</p>

---

##  ¿Qué es este proyecto?

**Inferno Colombia (Corte 2)** es una evolución del e-commerce original en PHP, migrado a **Python + FastAPI** con enfoque distribuido:

- Catálogo y vistas web con Jinja2
- API REST de productos
- Carrito y checkout
- **Checkout asíncrono** con cola de mensajes
- Estado de pedidos en tiempo real con Redis

---

##  Tabla de contenido

- [Arquitectura](#-arquitectura)
- [Componentes Clave](#-componentes-clave)
- [Flujo de Checkout Asíncrono](#-flujo-de-checkout-asíncrono)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Endpoints Principales](#-endpoints-principales)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [Demo Rápida](#-demo-rápida)
- [Troubleshooting](#-troubleshooting)
- [Autores](#-autores)

---

##  Arquitectura

```mermaid
flowchart LR
    C[Cliente Web / Swagger] --> API[FastAPI app.main]
    API --> MQ[(RabbitMQ\norders.create)]
    API --> R[(Redis\norder_status:{request_id})]
    API --> DB[(MySQL\nthreaderz_store)]

    W[Worker FastAPI\napp.worker] --> MQ
    W --> DB
    W --> R
```

### Modelo de comunicación

- **FastAPI** orquesta el flujo.
- **RabbitMQ** desacopla el request del procesamiento pesado de pedido.
- **Worker** consume eventos y persiste la orden en MySQL.
- **Redis** guarda el estado temporal del pedido (`PENDING`, `CONFIRMED`, `FAILED`).

---

##  Componentes Clave

- `fastapi_app/app/main.py` → API principal + rutas web + endpoint de estado de checkout.
- `fastapi_app/app/api_products.py` → API REST (`/productos`).
- `fastapi_app/app/queue.py` → publicación/consumo en RabbitMQ.
- `fastapi_app/app/worker.py` → procesamiento asíncrono de órdenes.
- `fastapi_app/app/order_status.py` → estado de órdenes en Redis.
- `fastapi_app/docker-compose.yml` → levanta Redis + RabbitMQ.

---

##  Flujo de Checkout Asíncrono

1. Usuario confirma compra en `/checkout?place=1`.
2. FastAPI publica mensaje en RabbitMQ (`orders.create`).
3. FastAPI registra estado en Redis: `order_status:{request_id}=PENDING`.
4. Front consulta `GET /checkout/status/{request_id}`.
5. Worker consume mensaje, crea orden en MySQL, limpia carrito.
6. Worker actualiza estado a `CONFIRMED` (o `FAILED`).
7. Cliente detecta estado final y redirige a pedidos.

---

##  Estructura del Proyecto

```text
Ecommerce-infernocol corte 2/
├── fastapi_app/
│   ├── app/
│   │   ├── main.py
│   │   ├── api_products.py
│   │   ├── queue.py
│   │   ├── worker.py
│   │   ├── order_status.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── settings.py
│   │   └── templates/
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── css/ js/ img/ fonts/
├── store.sql
└── (archivos PHP originales)
```

---

##  Endpoints Principales

### Web

- `GET /` Inicio
- `GET /shop` Tienda
- `GET /product/{product_id}` Detalle
- `GET /cart` Carrito
- `GET /checkout` Checkout
- `GET /checkout/status/{request_id}` Estado asíncrono

### API REST

- `POST /productos`
- `GET /productos`
- `GET /productos/{id}`

Swagger:

- `http://127.0.0.1:8000/docs`

---

##  Instalación y Ejecución

> Ejecutar desde `fastapi_app/`.

### 1) Preparar entorno

```powershell
cd "C:\xampp\htdocs\Ecommerce-infernocol corte 2\fastapi_app"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2) Configurar variables

```powershell
copy .env.example .env
```

Ajusta en `.env`:

- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `REDIS_HOST`, `REDIS_PORT`
- `RABBITMQ_HOST`, `RABBITMQ_PORT`
- (Opcional demo) `ORDER_PROCESSING_DELAY_SECONDS=40`

### 3) Levantar Redis + RabbitMQ

```powershell
docker compose up -d
```

RabbitMQ Management:

- `http://localhost:15672`
- user/pass: `guest` / `guest`

### 4) Ejecutar API y Worker

Terminal A:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal B:

```powershell
.\.venv\Scripts\python.exe -m app.worker
```

---

##  Demo Rápida

1. Inicia sesión.
2. Agrega producto al carrito.
3. Ve a Checkout y confirma pedido.
4. Se genera `request_id`.
5. Consulta en Swagger:
   - `GET /checkout/status/{request_id}`
6. Observa transición `PENDING` → `CONFIRMED`.

---

##  Troubleshooting

### `ModuleNotFoundError: No module named 'app'`
Ejecuta comandos dentro de `fastapi_app/`.

### `ModuleNotFoundError: No module named 'redis'`
Usa el Python del venv:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### El worker no imprime nada
Es normal: está esperando mensajes en cola.

---

##  Autores

- **Esteban Murillo Gomez**
- **Miguel Angel Villamil Echavarria**

---
