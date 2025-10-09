from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .db import engine
from .routers import router
from .config import settings
from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Haris API", version="0.4.0", lifespan=lifespan)

# metrics before startup
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# CORS from env
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "allowed_origins", ["*"]),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello, Haris 🚀"}

app.include_router(router)
