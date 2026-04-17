import json
import time
import re
from supabase import create_client, Client
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

SUPABASE_URL = "https://czijwystlhinkdhrpbnh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN6aWp3eXN0bGhpbmtkaHJwYm5oIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTUxMjE1NSwiZXhwIjoyMDkxMDg4MTU1fQ.JJHUIJSDQtTG0QyvOK3ZZDoxNC5wVaeG1SecUOqWFBU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
llm = OllamaLLM(model="llama3", temperature=0.0, format="json")

template = """
Analise o discurso parlamentar e extraia as informações solicitadas.

RETORNO ESPERADO (JSON):
{{
  "raciocinio_livre": "Pense em voz alta sobre o texto (MÁXIMO DE 3 FRASES).",
  "postura_extraida": "FAVORÁVEL ou CONTRÁRIO",
  "topico_identificado": "Escolha APENAS UMA tag: [Economia, Saúde, Educação, Segurança, Infraestrutura, Meio Ambiente, Direitos Humanos, Corrupção, Outros]",
  "justificativa": "Resuma o motivo em no máximo 15 palavras."
}}

REGRAS:
- A 'postura_extraida' deve refletir a intenção final do parlamentar.
- Ignore ataques a opositores; foque estritamente no tema central.
- O 'topico_identificado' DEVE ser uma opção exata da lista.
- Responda estritamente no formato JSON, sem nenhum texto extra.

Discurso: {discurso}
"""

prompt = PromptTemplate.from_template(template)
chain = prompt | llm

def limpar_saida_llm(texto_bruto):
    """Procura e extrai apenas o bloco JSON dentro do texto livre da IA."""
    # Encontra o primeiro '{' e o último '}'
    inicio = texto_bruto.find('{')
    fim = texto_bruto.rfind('}')
    
    if inicio != -1 and fim != -1:
        return texto_bruto[inicio:fim+1]
    
    return texto_bruto # Retorna do jeito que veio se der ruim

def calcular_coerencia_booleana(postura_ia, voto_oficial):
    if not postura_ia or not voto_oficial or str(voto_oficial).strip() == "None" or str(voto_oficial).strip() == "NULL":
        return None
        
    postura = str(postura_ia).strip().upper()
    voto = str(voto_oficial).strip().upper()

    if (postura == "FAVORÁVEL" and voto == "SIM") or (postura == "CONTRÁRIO" and voto == "NÃO"):
        return True
    else:
        return False

def rodar_fase_ia():
    print("🧠 FASE 1: Buscando discursos novos para análise da IA...")
    try:
        resposta_db = supabase.table("provas_contradicao").select("*").is_("postura_extraida", "null").execute()
        pendentes = resposta_db.data
    except Exception as e:
        print(f"❌ Erro ao conectar com Supabase na Fase 1: {e}")
        return

    if not pendentes:
        print("   ✅ Nenhum texto novo para a IA ler.")
        return

    for linha in pendentes:
        id_registro = linha.get('id')
        texto = linha.get('texto_extraido')
        
        if not texto or str(texto).strip() == "None":
            continue
            
        print(f"   ↳ Lendo ID {id_registro} com Llama 3...")
        try:
            resposta_ia = chain.invoke({"discurso": texto})

            # ==========================================
            # 🔍 LUPA DE DEBUG: Printando o texto cru da IA
            # ==========================================
            print(f"\n--- 🕵️ RAW DA IA (ID {id_registro}) ---")
            print(resposta_ia)
            print("----------------------------------\n")
            # ==========================================
            
            # --- O NOVO ESCUDO ---
            json_limpo = limpar_saida_llm(resposta_ia)
            dados_extraidos = json.loads(json_limpo)
            # ---------------------
            
            if "raciocinio_livre" in dados_extraidos:
                del dados_extraidos["raciocinio_livre"]
            
            supabase.table("provas_contradicao").update({
                "postura_extraida": dados_extraidos.get("postura_extraida"),
                "topico_identificado": dados_extraidos.get("topico_identificado"),
                "justificativa": dados_extraidos.get("justificativa")
            }).eq("id", id_registro).execute()
            
            print(f"      ✔ IA concluiu ID {id_registro} | Tópico: {dados_extraidos.get('topico_identificado')}")
            
        except json.JSONDecodeError:
            print(f"   ❌ Erro (ID {id_registro}): IA não retornou um JSON válido.")
        except Exception as e:
            print(f"   ❌ Erro na IA (ID {id_registro}): {e}")

def rodar_fase_logica():
    print("⚡ FASE 2: Cruzando posturas com votos no painel...")
    
    try:
        resposta_db = supabase.table("provas_contradicao").select("id, postura_extraida, voto_oficial") \
            .is_("status_coerencia", "null") \
            .not_.is_("postura_extraida", "null") \
            .not_.is_("voto_oficial", "null") \
            .execute()
        pendentes_logica = resposta_db.data
    except Exception as e:
        print(f"❌ Erro ao conectar com Supabase na Fase 2: {e}")
        return

    if not pendentes_logica:
        print("   ✅ Nenhum cruzamento lógico pendente.")
        return

    for linha in pendentes_logica:
        id_registro = linha['id']
        postura = linha['postura_extraida']
        voto = linha['voto_oficial']
        
        status = calcular_coerencia_booleana(postura, voto)
        
        if status is not None:
            supabase.table("provas_contradicao").update({
                "status_coerencia": status
            }).eq("id", id_registro).execute()
            print(f"   ↳ ID {id_registro} atualizado! Postura: {postura} | Voto: {voto} -> Coerente: {status}")

def processar_lote():
    print("INICIANDO WORKER DE ETL - CONTRADITO 🚀")
    print("=" * 50)
    inicio = time.time()
    
    rodar_fase_ia()       
    print("-" * 50)
    rodar_fase_logica()   
    
    fim = time.time()
    print("=" * 50)
    print(f"🏁 Worker finalizado com sucesso em {fim - inicio:.1f} segundos.")

if __name__ == "__main__":
    processar_lote()