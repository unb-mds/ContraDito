from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.bancos.supabase import supabase
from datetime import datetime

router = APIRouter(prefix="/api/logs", tags=["Monitoramento"])


class LogIA(BaseModel):
    id_parlamentar: int
    tipo_erro: str
    detalhes: str


@router.post("/falhas", status_code=201)
def registrar_falha_ia(log: LogIA):
    try:
        dados = {
            "id_parlamentar": log.id_parlamentar,
            "tipo_erro": log.tipo_erro,
            "detalhes": log.detalhes,
        }
        res = supabase.table("logs_pipeline_ia").insert(dados).execute()
        return {"mensagem": "Log registrado com sucesso", "dados": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar log: {str(e)}")


@router.get("/falhas")
def listar_falhas(limite: int = 50):
    try:
        res = (
            supabase.table("logs_pipeline_ia")
            .select("*")
            .order("id", desc=True)
            .limit(limite)
            .execute()
        )
        return {"total_erros_recentes": len(res.data), "logs": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar logs: {str(e)}")
