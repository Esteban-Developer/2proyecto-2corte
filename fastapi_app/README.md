# FastAPI migration (Inferno Colombia)

Este directorio contiene la migración del ecommerce PHP a **Python + FastAPI**, reutilizando los assets existentes (`/css`, `/js`, `/img`, `/fonts`) y la base de datos MySQL `threaderz_store`.

## Requisitos

- Python 3.10+
- MySQL (XAMPP)
- Base de datos importada desde `store.sql` (en la raíz del repo)

## Configuración

Crea un archivo `.env` dentro de `fastapi_app/` (puedes copiar `.env.example`) y ajusta credenciales.

## Instalación

```bash
cd fastapi_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install itsdangerous
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Ejecutar

```bash
cd fastapi_app
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Luego abre `http://127.0.0.1:8000/`.

## Rutas principales

- `/` Inicio
- `/shop` Tienda (paginación y filtros `cat_id`, `p_cat_id`, `page`)
- `/product/{product_id}` Detalle producto
- `/cart` Carrito
- `/checkout` Checkout
- `/login`, `/register`, `/logout`
- `/account?orders=1` y `/account?details=1`
- `/contact`
- `/admin/insert-product`

## Notas

- Autenticación: se replica el comportamiento del PHP, usando cookie de sesión y `customer_email` como identificador.
- Contraseñas: la BD actual guarda `customer_pass` en texto plano (como en el PHP).
