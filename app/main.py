from fastapi import FastAPI
app = FastAPI(title="Haris API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello, Haris 🚀"}
