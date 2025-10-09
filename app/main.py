from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .db import engine
from .routers import router

app = FastAPI(title="Haris API", version="0.3.0")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# CORS (adjust origins later if you want stricter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
