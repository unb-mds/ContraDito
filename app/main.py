from fastapi import FastAPI
from app.rotas import politicos

app = FastAPI(
    title="API Coerência Política",
    description="Back-end oficial da Squad 9 para análise de discursos parlamentares",
    version="1.0.0",
)

app.include_router(politicos.router)


@app.get("/")
def home():
    return {"status": "Servidor rodando liso na arquitetura limpa!"}
