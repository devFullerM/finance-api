from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="Finance API",
    description="A personal finance tracking API",
    version="0.1.0"
)

app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}