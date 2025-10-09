from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from sqlalchemy import text
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from asgi_correlation_id import CorrelationIdMiddleware

from .db import engine
from .routers import router
from .config import settings
from .logging_setup import configure_logging
from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB tables
    SQLModel.metadata.create_all(engine)
    # Rate limiter (Redis)
    r = redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)
    yield
    await r.close()

# app
app = FastAPI(title="Haris API", version="0.5.0", lifespan=lifespan)

# metrics before startup
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# request IDs
app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "allowed_origins", ["*"]),
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON logs
configure_logging(settings.log_level)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    # ping DB
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ready"}

@app.get("/")
def root():
    return {"message": "Hello, Haris 🚀"}

# routes
app.include_router(router)
