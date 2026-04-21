from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.rotas import politicos, logs


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando o Cache em Memória...")
    FastAPICache.init(InMemoryBackend())

    yield

    print("Desligando a API...")


app = FastAPI(
    title="API Coerência Política",
    description="Back-end oficial da Squad 9 para análise de discursos parlamentares",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(politicos.router)
app.include_router(logs.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "Servidor rodando liso na arquitetura limpa!"}
