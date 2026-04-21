import math
from fastapi import APIRouter, Query, HTTPException, Path
from typing import Optional
from app.bancos.supabase import supabase
from fastapi_cache.decorator import cache
from app.modelos.schemas import (
    PaginaPoliticos,
    PoliticoResponse,
    PerfilPoliticoDetalhado,
    ProvaContradicao,
    ContextoOriginal,
    ResultadoIA,
)
# Cria o roteador pro main.py
router = APIRouter(prefix="/api/politicos", tags=["Políticos"])


@router.get("", response_model=PaginaPoliticos)
@cache(expire=3600)
def listar_politicos(
    busca: Optional[str] = Query(None, description="Busca por nome de urna"),
    partido: Optional[str] = Query(None, description="Filtro por partido"),
    cargo: Optional[str] = Query(None, description="Filtro por cargo"),
    uf: Optional[str] = Query(
        None, min_length=2, max_length=2, description="Filtro por Estado/UF"
    ),
    ordem: Optional[str] = Query(
        None, description="Ordenação: 'mais_coerentes' ou 'menos_coerentes'"
    ),
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho: int = Query(
        20, ge=1, le=100, description="Quantidade de itens por página"
    ),
):
    try:
        query = supabase.table("politicos").select("*", count="exact")

        if busca:
            query = query.ilike("nome_urna", f"%{busca}%")
        if partido:
            query = query.eq("partido", partido.upper())
        if cargo:
            query = query.eq("cargo", cargo)
        if uf:
            query = query.eq("uf", uf.upper())

        if ordem == "mais_coerentes":
            query = query.order("score_coerencia", desc=True)
        elif ordem == "menos_coerentes":
            query = query.order("score_coerencia", desc=False)
        else:
            query = query.order("nome_urna", desc=False)

        inicio = (pagina - 1) * tamanho
        fim = inicio + tamanho - 1
        query = query.range(inicio, fim)

        resultado = query.execute()

        total_registros = resultado.count if resultado.count is not None else 0
        total_paginas = (
            math.ceil(total_registros / tamanho) if total_registros > 0 else 0
        )

        return {
            "total_registros": total_registros,
            "pagina_atual": pagina,
            "tamanho_pagina": tamanho,
            "total_paginas": total_paginas,
            "itens": resultado.data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/{id_parlamentar}", response_model=PerfilPoliticoDetalhado)
def buscar_politico_detalhado(
    id_parlamentar: int = Path(..., description="ID interno do político")
):
    res_politico = (
        supabase.table("politicos").select("*").eq("id", id_parlamentar).execute()
    )

    if not res_politico.data:
        raise HTTPException(status_code=404, detail="Político não encontrado")

    politico_data = res_politico.data[0]

    res_provas = (
        supabase.table("provas_contradicao")
        .select("*")
        .eq("politico_id", id_parlamentar)
        .execute()
    )

    provas_formatadas = []
    for p in res_provas.data:
        provas_formatadas.append(
            ProvaContradicao(
                id=p["id"],
                contexto=ContextoOriginal(
                    tipo_documento=p.get("tipo_documento", "Desconhecido"),
                    data_evento=p.get("data_evento", "Data não registrada"),
                    texto_extraido=p.get("texto_extraido", "Texto indisponível"),
                    link_fonte=p.get("link_fonte"),
                ),
                resultado=ResultadoIA(
                    topico_identificado=p.get(
                        "topico_identificado", "Tópico não identificado"
                    ),
                    postura_extraida_do_texto=p.get(
                        "postura_extraida_do_texto", "Postura não registrada"
                    ),
                    justificativa=p.get("justificativa"),
                    voto_oficial_registrado=p.get(
                        "voto_oficial_registrado", "Não registrado"
                    ),
                    status_coerencia=p.get("status_coerencia") is True,
                ),
            )
        )

    return PerfilPoliticoDetalhado(
        politico=PoliticoResponse(**politico_data), provas=provas_formatadas
    )
