# Como Calculamos o Score de Coerência

O **Score de Coerência** é a principal métrica do ContraDito. Ele não é baseado em opiniões políticas, mas sim num cruzamento analítico, semântico e matemático entre o que o parlamentar afirma nos seus discursos e como ele efetivamente vota nos projetos de lei.

Abaixo, detalhamos o passo a passo de como a nossa arquitetura de Inteligência Artificial e o nosso motor de busca vetorial chegam à nota final.

---

## O Fluxo de Cálculo (Passo a Passo)

### 1. Vetorização Semântica (O "Dito")
Primeiro, coletamos os discursos oficiais do parlamentar na Câmara dos Deputados. Após a limpeza de ruídos, o texto não é classificado por tags rígidas. Utilizamos o modelo **SBERT** (`paraphrase-multilingual-mpnet-base-v2`) para converter o discurso num **Embedding** (um vetor matemático de 768 dimensões). 
Este processo transforma o significado e a intenção da fala em coordenadas matemáticas, preservando nuances que uma simples tag ignoraria.

### 2. Mapeamento de Votos Oficiais (O "Feito")
Em paralelo, o nosso banco de dados mapeia os votos oficiais (Sim, Não ou Abstenção) em Projetos de Lei (PLs). A ementa de cada projeto também é convertida num vetor matemático através do mesmo modelo de embeddings, garantindo que "Dito" e "Feito" falem a mesma linguagem matemática.

### 3. O Cruzamento Matemático (O *Match*)
O motor do ContraDito utiliza a extensão **`pgvector`** no Supabase para calcular a **Similaridade de Cosseno** entre os vetores. 
* Se a similaridade é alta, significa que o discurso e a lei tratam do mesmo assunto semântico.
* O sistema recupera esse "par ideal" e aciona o **Llama 3** para confirmar a consistência:
    * **Coerência Positiva:** O discurso defende a pauta e o voto foi favorável (ou vice-versa).
    * **Contradição (Incoerência):** O discurso aponta para um lado, mas o voto registado foi na direção oposta.

### 4. A Fórmula Matemática do Score
O *Score de Coerência* é uma nota de **[0 a 100]**, calculada com base no percentual de consistência nos cruzamentos validados pela busca vetorial.

*Fórmula simplificada:*
**Score = (Total de Ações Coerentes / Total de Cruzamentos Válidos) * 100**

*Exemplo Prático:*
> Se o sistema identificou 10 cruzamentos com alta similaridade semântica, e em 8 deles o parlamentar foi coerente entre fala e voto, o seu Score será **80**.

---

## Limitações e Mitigações
Para garantir justiça e evitar punições por mudanças naturais de contexto:
* **Fator Temporal:** Priorizamos cruzamentos entre discursos e votos próximos no tempo ou dentro da mesma legislatura.
* **Contexto Político:** O motor LLM analisa se votos em "Destaques" ou manobras regimentais justificam uma aparente mudança de posicionamento, garantindo que a nota reflita a intenção real.

---

## Os Bastidores do Passo 1: O Script de Extração (Seeder)

Para garantir que o processamento vetorial não seja prejudicado por ruídos protocolares (como "Obrigado, Sr. Presidente"), aplicamos regras de negócio diretamente no código de extração:

1. **Filtro de Relevância:** O script ignora automaticamente qualquer transcrição excessivamente curta (abaixo de 150 caracteres).
2. **Preparação de Dados:** O objeto do político é inicializado e as tabelas de provas são preparadas para receber os novos cruzamentos.
3. **Idempotência (Upsert):** Utilizamos a função `.upsert()` para garantir que atualizações de discursos não gerem duplicidade de registros.

**Trecho de destaque (Filtro de Ruído em Python):**
```python
def buscar_ultimo_discurso_relevante(id_camara):
    # ... (conexão com API) ...
    for discurso in dados:
        texto = discurso.get("transcricao", "")
        data_hora = discurso.get("dataHoraInicio", "2023-01-01T00:00").split("T")[0]

        # Regra de Negócio: Ignora discursos curtos/protocolares
        if len(texto) > 150:
            return texto, data_hora

    return "Nenhum discurso relevante encontrado.", "2023-01-01"
