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

## Developer shortcuts
```
make run   # compose up --build
make up    # start detached
make down  # stop
make logs  # tail logs
make test  # run pytest
make lint  # black + ruff
```

