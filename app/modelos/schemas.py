from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class PoliticoBase(BaseModel):
    nome_civil: str = Field(..., description="Nome oficial do parlamentar")
    nome_urna: str = Field(..., description="Nome utilizado na urna (usado na busca global)")
    cargo: str
    partido: str
    uf: str = Field(..., min_length=2, max_length=2, description="Sigla do Estado (ex: DF, SP)")
    foto_url: Optional[str] = None
    situacao: Optional[str] = None

class PoliticoResponse(PoliticoBase):
    id: int
    score_coerencia: float

class ContextoOriginal(BaseModel):
    tipo_documento: str
    data_evento: date
    texto_extraido: str
    link_fonte: Optional[str] = Field(None, description="Link do YouTube da TV Câmara ou PDF")

class ResultadoIA(BaseModel):
    topico_identificado: str
    postura_extraida_do_texto: str
    voto_oficial_registrado: str
    status_coerencia: bool

class ProvaContradicao(BaseModel):
    id: int
    contexto: ContextoOriginal
    resultado: ResultadoIA

class PerfilPoliticoDetalhado(BaseModel):
    politico: PoliticoResponse
    provas: List[ProvaContradicao]

class PaginaPoliticos(BaseModel):
    total_registros: int
    pagina_atual: int
    tamanho_pagina: int
    total_paginas: int
    itens: List[PoliticoResponse]