from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.motor_nlp import MotorNLP  

app = FastAPI(title="Microservico NLP - Worker")

print("Carregando modelo SBERT no Worker...")
motor_ia = MotorNLP()

class RequisicaoTexto(BaseModel):
    texto: str

@app.post("/gerar-embedding")
async def endpoint_gerar_embedding(req: RequisicaoTexto):
    if not req.texto or not req.texto.strip():
        raise HTTPException(status_code=400, detail="Texto vazio")
        
    vetor = await motor_ia.gerar_embedding(req.texto)
    
    return {"embedding": vetor}