import sys
import httpx
from pprint import pprint
from app.bancos.supabase import supabase

sys.stdout.reconfigure(encoding="utf-8")
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def buscar_ultimo_discurso_relevante(id_camara):
    """Busca o último discurso do parlamentar, a data e filtra ruídos protocolares."""
    try:
        resp = httpx.get(
            f"{BASE_URL}/deputados/{id_camara}/discursos",
            params={"itens": 5, "ordem": "DESC", "dataInicio": "2023-01-01"},
            headers={"Accept": "application/json"},
            timeout=30.0,
        )
        resp.raise_for_status()
        dados = resp.json().get("dados", [])

        for discurso in dados:
            texto = discurso.get("transcricao", "")
            data_hora = discurso.get("dataHoraInicio", "2023-01-01T00:00").split("T")[0]

            if len(texto) > 150:
                return texto, data_hora

        return "Nenhum discurso relevante encontrado após aplicar os filtros.", "2023-01-01"
    except Exception as e:
        return f"Erro ao buscar discurso: {e}", "2023-01-01"


def buscar_amostra_deputados(quantidade=20):
    print(f"🔍 Buscando {quantidade} deputados na API da Câmara...")

    resposta = httpx.get(
        f"{BASE_URL}/deputados",
        params={"itens": quantidade},
        headers={"Accept": "application/json"},
        timeout=30.0,
    )
    resposta.raise_for_status()
    lista_basica = resposta.json()["dados"]

    lista_politicos = []
    lista_provas = []

    for dep in lista_basica:
        id_camara = dep["id"]
        print(f"Extraindo detalhes e discursos do deputado ID: {id_camara}...")

        detalhe_resp = httpx.get(
            f"{BASE_URL}/deputados/{id_camara}",
            headers={"Accept": "application/json"},
            timeout=30.0,
        )
        dados_completos = detalhe_resp.json()["dados"]
        status = dados_completos["ultimoStatus"]

        texto_discurso, data_discurso = buscar_ultimo_discurso_relevante(id_camara)

        politico = {
            "id": id_camara,
            "nome_civil": dados_completos.get("nomeCivil", ""),
            "nome_urna": status.get("nomeEleitoral", ""),
            "cargo": "Deputado Federal",
            "partido": status.get("siglaPartido", ""),
            "uf": status.get("siglaUf", ""),
            "foto_url": status.get("urlFoto", ""),
            "situacao": status.get("situacao", ""),
            "score_coerencia": 0.0,
        }
        lista_politicos.append(politico)

        prova = {
            "politico_id": id_camara,
            "tipo_documento": "Discurso",
            "data_evento": data_discurso,
            "texto_extraido": texto_discurso,
            "link_fonte": f"https://www.camara.leg.br/deputados/{id_camara}",
            "topico_identificado": None,
            "postura_extraida": None,
            "voto_oficial": None,
            "status_coerencia": None,  
            "justificativa": None
        }

        lista_provas.append(prova)

    # Retorna as duas listas prontas para o banco
    return lista_politicos, lista_provas


def salvar_no_supabase(lista_politicos, lista_provas):
    print("\n🚀 Iniciando Processamento (Upsert) no Banco de Dados...")

    try:
        # Trocamos .insert() por .upsert()
        # O parâmetro on_conflict='id' avisa ao Supabase: 
        # "Se o ID já existir, atualize os campos. Se não existir, insira."
        resp_politicos = supabase.table("politicos").upsert(
            lista_politicos, 
            on_conflict='id'
        ).execute()
        print(f"✅ Sucesso! {len(resp_politicos.data)} políticos processados (inseridos ou atualizados).")

        # Fazemos o mesmo para a tabela de provas
        # Isso permite que você rode o seeder várias vezes sem duplicar as provas de um mesmo discurso
        resp_provas = supabase.table("provas_contradicao").upsert(
            lista_provas
        ).execute()
        print(f"✅ Sucesso! {len(resp_provas.data)} provas vinculadas e prontas para a IA.")
        
    except Exception as e:
        print(f"❌ Ocorreu um erro ao salvar no banco: {e}")


if __name__ == "__main__":
    # Executa a extração, separando políticos e provas
    politicos, provas = buscar_amostra_deputados(513)
    
    # Envia os pacotes completos para o Supabase
    salvar_no_supabase(politicos, provas)
