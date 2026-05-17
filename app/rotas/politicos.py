import math
from fastapi import APIRouter, Query, HTTPException, Path, Request
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.bancos.supabase import supabase
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from collections import defaultdict
import httpx
from app.modelos.schemas import (
    PaginaPoliticos,
    PoliticoResponse,
    PerfilPoliticoDetalhado,
    ProvaContradicao,
    ContextoOriginal,
    ResultadoIA,
    BuscaVetorialRequest,
    ResultadoSimilaridade,
)

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/politicos", tags=["Políticos"])


@router.get(
    "",
    response_model=PaginaPoliticos,
    summary="Listar e Filtrar Políticos",
    description="Retorna a listagem paginada de parlamentares. Permite filtros combinados (Nome, Partido, UF, Cargo) e ordenação pelo Score de Coerência.",
    response_description="Objeto com metadados de paginação e a lista de políticos.",
)
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


@router.get(
    "/{id_parlamentar}",
    response_model=PerfilPoliticoDetalhado,
    summary="Obter Perfil Detalhado",
    description="Retorna os dados cadastrais de um político específico junto com seu histórico de checagem de fatos (Provas de Contradição).",
    responses={
        404: {"description": "Político não encontrado na base de dados."},
    },
)
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


@router.post(
    "/buscar-similares",
    response_model=list[ResultadoSimilaridade],
    summary="Busca Semântica no Banco Vetorial",
    description="""
    Recebe um texto de busca (ex: ementa de lei), envia para o Worker NLP gerar o Embedding e executa
    uma Stored Procedure (RPC) no Supabase para retornar os discursos mais próximos matematicamente.
    Se não encontrar nenhum discurso acima do limiar, retorna um array vazio.
    """,
    responses={
        400: {"description": "Texto vazio ou falha na geração do vetor pela IA."},
        503: {"description": "Worker de NLP indisponível (Timeout)."},
    },
)
@limiter.limit("5/minute")
async def buscar_discursos_por_similaridade(
    request: Request, requisicao: BuscaVetorialRequest
):
    try:
        async with httpx.AsyncClient() as client:
            try:
                resposta_worker = await client.post(
                    "http://worker:8001/gerar-embedding",
                    json={"texto": requisicao.texto_busca},
                    timeout=8.0,
                )
                resposta_worker.raise_for_status()
            except httpx.RequestError:
                raise HTTPException(
                    status_code=503, detail="Serviço NLP indisponível no Worker."
                )

            dados_ia = resposta_worker.json()
            vetor_real = dados_ia.get("embedding")

            if not vetor_real:
                raise HTTPException(
                    status_code=400,
                    detail="A IA não conseguiu processar o texto de busca.",
                )

        parametros_rpc = {
            "query_embedding": vetor_real,
            "match_threshold": 0.2,
            "match_count": requisicao.limite,
            "p_politico_id": requisicao.id_parlamentar,
        }

        resposta_rpc = supabase.rpc(
            "buscar_discursos_similares", parametros_rpc
        ).execute()

        return resposta_rpc.data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno na busca vetorial: {str(e)}"
        )


@router.post(
    "/interno/recalcular-scores",
    summary="Recalcula o Score de todos os políticos (Uso Interno)",
    description="Rota chamada pelo ETL após o cruzamento de dados. Aplica o RF15 e RF27, salvando o resultado direto na tabela 'politicos'.",
    include_in_schema=False,  # Esconde a rota do Swagger público
)
def recalcular_todos_scores():
    try:
        # 1. Puxa do banco apenas as provas que já passaram pela IA e pela Fase Lógica
        resposta_db = (
            supabase.table("provas_contradicao")
            .select("politico_id, status_coerencia, voto_oficial")
            .not_.is_("status_coerencia", "null")
            .execute()
        )

        provas = resposta_db.data

        # 2. Agrupa o histórico de votos pelo ID do político
        historico_por_politico = defaultdict(list)
        for p in provas:
            historico_por_politico[p["politico_id"]].append(p)

        # O limite que conversamos para o político não ficar com "Score Nulo"
        VOLUME_MINIMO_ACEITAVEL = 3

        # 3. Varre o agrupamento de cada político
        for id_politico, lista_provas in historico_por_politico.items():
            votos_coerentes = 0
            total_validos = 0

            for prova in lista_provas:
                voto = str(prova.get("voto_oficial")).strip().upper()

                # RF27: Ignora abstenções e faltas (não entram no denominador)
                if voto in [
                    "AUSENTE",
                    "ABSTENÇÃO",
                    "ABSTENCAO",
                    "NÃO COMPARECEU",
                    "NONE",
                    "NULL",
                ]:
                    continue

                total_validos += 1

                # Conta os acertos
                if prova.get("status_coerencia") is True:
                    votos_coerentes += 1

            # RF15: Avalia o volume de dados mínimos
            if total_validos < VOLUME_MINIMO_ACEITAVEL:
                score_final = None
            else:
                score_final = round((votos_coerentes / total_validos) * 100, 1)

            # 4. Grava o valor definitivo na tabela 'politicos'
            supabase.table("politicos").update({"score_coerencia": score_final}).eq(
                "id", id_politico
            ).execute()

        return {
            "status": "sucesso",
            "mensagem": f"Scores de {len(historico_por_politico)} políticos recalculados.",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao recalcular scores: {str(e)}"
        )


@router.post(
    "/interno/limpar-cache",
    summary="Invalida o cache global da API (Uso Interno)",
    description="Limpa o InMemoryBackend. Chamado pelo ETL para garantir dados frescos no Front-end.",
    include_in_schema=False,
)
async def limpar_cache_global():
    try:
        await FastAPICache.clear()
        return {
            "status": "sucesso",
            "mensagem": "Cache global limpo com sucesso. O Front-end agora receberá dados frescos.",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar cache: {str(e)}")
