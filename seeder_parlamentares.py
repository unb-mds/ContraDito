import sys
import httpx
import asyncio
import hashlib
from app.bancos.supabase import supabase

sys.stdout.reconfigure(encoding="utf-8")
BASE_URL_CAMARA = "https://dadosabertos.camara.leg.br/api/v2"
BASE_URL_SENADO = "https://legis.senado.leg.br/dadosabertos"

# Evita colisão de IDs no banco (Senador ID 500 vira 1000500)
OFFSET_ID_SENADO = 1000000 

# Filtro para ignorar leituras protocolares
STOP_PHRASES = [
    "declaro aberta a sessão", "passo a palavra", "pela ordem",
    "peço a palavra", "minuto de silêncio", "sessão solene",
    "sob a proteção de deus", "lista de presença", "horário destinado",
    "encerro a sessão", "parecer de redação", "leitura da ata"
]

def eh_discurso_valido(texto):
    if not texto or len(texto) < 150:
        return False
        
    texto_lower = texto.lower()
    for phrase in STOP_PHRASES:
        if phrase in texto_lower:
            return False
    return True

def gerar_hash_discurso(texto):
    """Gera um MD5 do texto para evitar limite de 2704 bytes de indexação do B-Tree no Postgres."""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

# ==========================================
# CÂMARA DOS DEPUTADOS
# ==========================================
async def buscar_discursos_camara(client, id_camara, qtd_desejada=3):
    try:
        resp = await client.get(
            f"{BASE_URL_CAMARA}/deputados/{id_camara}/discursos",
            params={"itens": 20, "ordem": "DESC", "dataInicio": "2023-01-01"},
        )
        resp.raise_for_status()
        dados = resp.json().get("dados", [])

        discursos_validos = []
        for d in dados:
            texto = d.get("transcricao", "")
            data_hora = d.get("dataHoraInicio", "2023-01-01T00:00").split("T")[0]

            if eh_discurso_valido(texto):
                discursos_validos.append((texto, data_hora))
                if len(discursos_validos) == qtd_desejada:
                    break
        return discursos_validos
    except Exception:
        return []

async def processar_deputado(client, dep, semaphore, lista_politicos, lista_provas):
    id_camara = dep["id"]
    async with semaphore: # Semáforo para evitar bloqueio por Rate Limit na API
        try:
            detalhe_resp = await client.get(f"{BASE_URL_CAMARA}/deputados/{id_camara}")
            detalhe_resp.raise_for_status()
            dados_completos = detalhe_resp.json()["dados"]
            status = dados_completos["ultimoStatus"]

            discursos = await buscar_discursos_camara(client, id_camara, qtd_desejada=3)
            nome_urna = status.get("nomeEleitoral", f"ID {id_camara}")

            lista_politicos.append({
                "id": id_camara,
                "nome_civil": dados_completos.get("nomeCivil", ""),
                "nome_urna": nome_urna,
                "cargo": "Deputado Federal",
                "partido": status.get("siglaPartido", ""),
                "uf": status.get("siglaUf", ""),
                "foto_url": status.get("urlFoto", ""),
                "situacao": status.get("situacao", ""),
                "score_coerencia": 0.0,
            })

            for texto, data in discursos:
                lista_provas.append({
                    "politico_id": id_camara,
                    "tipo_documento": "Discurso",
                    "data_evento": data,
                    "texto_extraido": texto,
                    "hash_discurso": gerar_hash_discurso(texto),
                    "link_fonte": f"https://www.camara.leg.br/deputados/{id_camara}",
                })
            print(f"✅ Câmara | {nome_urna} ({len(discursos)} discursos)")
        except Exception as e:
            print(f"❌ Erro deputado {id_camara}: {e}")

async def buscar_amostra_deputados(quantidade=513):
    async with httpx.AsyncClient(timeout=45.0) as client:
        resposta = await client.get(f"{BASE_URL_CAMARA}/deputados", params={"itens": quantidade})
        lista_basica = resposta.json()["dados"]
        
        lista_politicos, lista_provas = [], []
        semaphore = asyncio.Semaphore(15)
        
        tarefas = [processar_deputado(client, dep, semaphore, lista_politicos, lista_provas) for dep in lista_basica]
        await asyncio.gather(*tarefas)

    return lista_politicos, lista_provas

# ==========================================
# SENADO FEDERAL
# ==========================================
async def buscar_discursos_senado(client, id_senado_original, qtd_desejada=3):
    try:
        resp = await client.get(
            f"{BASE_URL_SENADO}/senador/{id_senado_original}/discursos.json",
            headers={"Accept": "application/json"}
        )
        if resp.status_code != 200:
            return []

        dados = resp.json()
        discursos_node = dados.get("DiscursosParlamentar", {}).get("Parlamentar", {}).get("Pronunciamentos", {}).get("Pronunciamento", [])
        
        if isinstance(discursos_node, dict):
            discursos_node = [discursos_node]

        discursos_validos = []
        for d in discursos_node:
            texto = d.get("TextoIntegral") or d.get("ResumoPronunciamento", "")
            data_hora = d.get("DataPronunciamento", "2023-01-01").split(" ")[0]

            if eh_discurso_valido(texto):
                discursos_validos.append((texto, data_hora))
                if len(discursos_validos) == qtd_desejada:
                    break
        return discursos_validos
    except Exception:
        return []

async def processar_senador(client, senador_data, semaphore, lista_politicos, lista_provas):
    identificacao = senador_data.get("IdentificacaoParlamentar", {})
    id_senado_original = int(identificacao.get("CodigoParlamentar"))
    id_banco = id_senado_original + OFFSET_ID_SENADO

    async with semaphore:
        try:
            discursos = await buscar_discursos_senado(client, id_senado_original, qtd_desejada=3)
            nome_urna = identificacao.get("NomeParlamentar", "")

            lista_politicos.append({
                "id": id_banco,
                "nome_civil": identificacao.get("NomeCompletoParlamentar", ""),
                "nome_urna": nome_urna,
                "cargo": "Senador",
                "partido": identificacao.get("SiglaPartidoParlamentar", ""),
                "uf": identificacao.get("UfParlamentar", ""),
                "foto_url": identificacao.get("UrlFotoParlamentar", ""),
                "situacao": "Em Exercício",
                "score_coerencia": 0.0,
            })

            for texto, data in discursos:
                lista_provas.append({
                    "politico_id": id_banco,
                    "tipo_documento": "Discurso",
                    "data_evento": data,
                    "texto_extraido": texto,
                    "hash_discurso": gerar_hash_discurso(texto),
                    "link_fonte": f"https://www25.senado.leg.br/web/senadores/senador/-/perfil/{id_senado_original}",
                })
            print(f"✅ Senado | {nome_urna} ({len(discursos)} discursos)")
        except Exception as e:
            print(f"❌ Erro senador {id_senado_original}: {e}")

async def buscar_amostra_senadores():
    async with httpx.AsyncClient(timeout=45.0) as client:
        resposta = await client.get(
            f"{BASE_URL_SENADO}/senador/lista/atual.json",
            headers={"Accept": "application/json"}
        )
        resposta.raise_for_status()

        lista_basica = resposta.json().get("ListaParlamentarEmExercicio", {}).get("Parlamentares", {}).get("Parlamentar", [])
        
        lista_politicos, lista_provas = [], []
        semaphore = asyncio.Semaphore(15)

        tarefas = [processar_senador(client, dep, semaphore, lista_politicos, lista_provas) for dep in lista_basica]
        await asyncio.gather(*tarefas)

    return lista_politicos, lista_provas

# ==========================================
# PERSISTÊNCIA NO BANCO
# ==========================================
def salvar_no_supabase(lista_politicos, lista_provas):
    print("\n🚀 Iniciando Upsert no Banco de Dados...")
    try:
        resp_politicos = supabase.table("politicos").upsert(lista_politicos, on_conflict='id').execute()
        print(f"✅ {len(resp_politicos.data)} políticos sincronizados.")

        for p in lista_provas:
            p.update({
                "topico_identificado": None, "postura_extraida": None,
                "voto_oficial": None, "status_coerencia": None, "justificativa": None
            })

        # on_conflict agora utiliza a regra atualizada com o hash
        resp_provas = supabase.table("provas_contradicao").upsert(
            lista_provas, on_conflict='politico_id, data_evento, hash_discurso'
        ).execute()
        print(f"✅ {len(resp_provas.data)} provas vinculadas com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")

# ==========================================
# ORQUESTRAÇÃO PRINCIPAL
# ==========================================
async def main():
    print("🚀 Iniciando extração do Congresso Nacional...")
    task_camara = buscar_amostra_deputados(513)
    task_senado = buscar_amostra_senadores()
    
    # Roda as extrações da Câmara e Senado em paralelo
    resultados_camara, resultados_senado = await asyncio.gather(task_camara, task_senado)

    todos_politicos = resultados_camara[0] + resultados_senado[0]
    todas_provas = resultados_camara[1] + resultados_senado[1]

    salvar_no_supabase(todos_politicos, todas_provas)
    print("🎉 Extração do Congresso finalizada com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
