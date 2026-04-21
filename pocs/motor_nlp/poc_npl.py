import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import time

with open('amostra_para_luiz.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)
    texto_discurso = dados['contexto_original']['texto_extraido']

llm = Ollama(model="llama3", temperature=0.0)

template = """
Você é um analista de dados políticos. 
Leia o discurso abaixo e extraia o tópico principal e a postura.

REGRAS DE CLASSIFICAÇÃO:
1. A postura (FAVORÁVEL, CONTRÁRIO, NEUTRO) deve ser ESTRITAMENTE em relação ao TÓPICO PRINCIPAL. 
2. Se o orador for favorável ao tópico, mas atacar opositores ou outros partidos no meio do texto, a postura sobre o tópico continua sendo FAVORÁVEL. Ignore os ataques pessoais.

Retorne APENAS um objeto JSON no formato exato: 
{{"raciocinio": "sua explicacao breve em uma frase", "topico": "...", "postura": "..."}}
Não escreva nenhuma palavra além do JSON.

Discurso:
{discurso}
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm

print("Processando o discurso")
resposta_texto = chain.invoke({"discurso": texto_discurso})

try:
    resultado_dict = json.loads(resposta_texto)
    
    if 'raciocinio' in resultado_dict:
        del resultado_dict['raciocinio']
    
    json_final = json.dumps(resultado_dict, indent=2, ensure_ascii=False)
    
    print("\n--- Resultado da IA (Limpo) ---")
    print(json_final)

except json.JSONDecodeError:
    print("\n[ERRO] A IA não retornou um JSON válido. Retorno bruto:")
    print(resposta_texto)