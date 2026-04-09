import httpx
from pprint import pprint

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

def buscar_ultimo_discurso(id_camara):
    """Busca o último discurso do parlamentar para alimentar a IA."""
    try:
        resp = httpx.get(
            f"{BASE_URL}/deputados/{id_camara}/discursos",
            params={"itens": 1, 
                    "ordem": "DESC",
                    "dataInicio": "2023-01-01"
            }, 
            headers={"Accept": "application/json"},
            timeout=30.0
        )
        resp.raise_for_status()
        dados = resp.json().get("dados", [])
        
        if dados and len(dados) > 0:
            # Retorna a transcrição do primeiro discurso da lista
            return dados[0].get("transcricao", "Discurso não transcrito na API.")
        return "Nenhum discurso encontrado."
    except Exception as e:
        return f"Erro ao buscar discurso: {e}"

def buscar_amostra_deputados(quantidade=20):
    print(f"🔍 Buscando {quantidade} deputados na API da Câmara...")
    
    resposta = httpx.get(
        f"{BASE_URL}/deputados", 
        params={"itens": quantidade},
        headers={"Accept": "application/json"},
        timeout=30.0
    )
    resposta.raise_for_status()
    lista_basica = resposta.json()["dados"]
    
    deputados_formatados = []
    
    for dep in lista_basica:
        id_camara = dep["id"]
        print(f"Extraindo detalhes e discursos do deputado ID: {id_camara}...")
        
        # 1. Busca os detalhes de perfil
        detalhe_resp = httpx.get(
            f"{BASE_URL}/deputados/{id_camara}",
            headers={"Accept": "application/json"},
            timeout=30.0
        )
        dados_completos = detalhe_resp.json()["dados"]
        status = dados_completos["ultimoStatus"]
        
        # 2. Busca o último discurso (A Mágica Nova!)
        texto_discurso = buscar_ultimo_discurso(id_camara)
        
        # 3. Monta o Dicionário completo
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
            "discurso_bruto": texto_discurso 
        }
        
        deputados_formatados.append(politico)
        
    return deputados_formatados

def salvar_no_supabase(lista_politicos):
    print("\n🚀 Iniciando Inserção no Banco de Dados...")
    for politico in lista_politicos:
        print(f"✅ [Mock DB] Preparado para o banco: {politico['nome_urna']} ({politico['partido']}-{politico['uf']})")

if __name__ == "__main__":
    amostra = buscar_amostra_deputados(20)
    salvar_no_supabase(amostra)
    
    print("\nExemplo da estrutura do primeiro político com discurso:")
    pprint(amostra[0])