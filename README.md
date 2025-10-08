# FastAPI Starter

Containerized FastAPI template with hot reload.

## Run (Docker)
~~~bash
docker compose up --build
# http://localhost:8000  |  /health
~~~

## Endpoints
- `GET /` → hello
- `GET /health` → `{ "status": "ok" }`
