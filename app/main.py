from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routers import auth, categories, transactions

security = HTTPBearer()

app = FastAPI(
    title="Finance API",
    description="A personal finance tracking API",
    version="0.1.0"
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}