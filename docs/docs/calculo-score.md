# Como Calculamos o Score de Coerência

O **Score de Coerência** é a principal métrica do ContraDito. Ele não é baseado em opiniões políticas, mas sim em um cruzamento analítico e matemático entre o **discurso público** (o que o político diz) e o **voto em plenário** (o que o político faz).

Abaixo, detalhamos o passo a passo de como a nossa Inteligência Artificial e o nosso motor de regras chegam à nota final de cada parlamentar.

---

## O Fluxo de Cálculo (Passo a Passo)

### 1. Extração de Entidades e Posicionamento (O "Dito")
Primeiro, coletamos os discursos oficiais do parlamentar na Câmara dos Deputados. Nossa Inteligência Artificial (modelo LLM rodando via Ollama) lê o texto e extrai três informações cruciais:
* **Tema/Tag:** Qual é o assunto principal? (ex: *Reforma Tributária*, *Privatização*, *Meio Ambiente*).
* **Posicionamento:** Qual a postura do político sobre o tema? (A favor, Contra ou Neutro).
* **Trecho (Evidência):** A frase exata que comprova esse posicionamento.

### 2. Mapeamento de Votos Oficiais (O "Feito")
Em paralelo, nosso banco de dados mapeia como esse mesmo parlamentar votou (Sim, Não ou Abstenção) em Projetos de Lei (PLs) e emendas que possuem as mesmas **Tags** identificadas nos discursos.

### 3. O Cruzamento de Dados (O *Match*)
O motor do ContraDito cruza a tag do discurso com a tag do voto e verifica a consistência:
* **Coerência Positiva:** Discursou "A favor" e votou "Sim" (ou discursou "Contra" e votou "Não").
* **Contradição (Incoerência):** Discursou "A favor" e votou "Não" (ou vice-versa).
* **Abstenção/Neutralidade:** Avaliada caso a caso dependendo do impacto da votação.

### 4. A Fórmula Matemática do Score
O *Score de Coerência* é uma nota de **[0 a 100]**, calculada com base no percentual de consistência entre os discursos e os votos atrelados à mesma tag. 

*Fórmula simplificada:*
**Score = (Total de Ações Coerentes / Total de Cruzamentos Válidos) * 100**

*Exemplo Prático:*
> Se o Deputado X possui 10 cruzamentos válidos (temas onde ele discursou E votou), e em 8 deles o voto seguiu o discurso, seu Score de Coerência será **80**. Os 2 casos divergentes serão listados no perfil dele como **"Provas da Contradição"**.

---

## Limitações e Mitigações
Reconhecemos que a política é dinâmica e os políticos podem mudar de opinião ao longo do tempo. Para garantir justiça no cálculo:
* **Fator Temporal:** Damos prioridade a cruzamentos de discursos e votos que ocorreram na mesma legislatura ou em um espaço de tempo próximo.
* **Contexto da Votação:** Votos em "Destaques" ou manobras regimentais (que às vezes obrigam o político a votar "Não" no texto-base para aprovar uma emenda) são tratados com cautela pelo nosso modelo para evitar falsos positivos de contradição.

### Os Bastidores do Passo 1: O Script de Extração (Seeder)

Para garantir que a Inteligência Artificial não perca tempo processando ruídos protocolares (como "Obrigado, Sr. Presidente" ou "Passo a palavra"), nosso script de extração em Python (`seeder.py`) atua como o primeiro filtro do sistema.

Abaixo, destacamos as regras de negócio aplicadas direto no código antes mesmo do dado chegar ao banco:

1. **Filtro de Relevância (Tamanho do Texto):** O script consome a API da Câmara (`/deputados/{id}/discursos`) e ignora automaticamente qualquer transcrição que tenha menos de 150 caracteres.
2. **Preparação para a IA:** O script cria o objeto do político inicializando o `score_coerencia` zerado e cria um registro na tabela `provas_contradicao` com os campos de análise (`topico_identificado`, `postura_extraida`, `voto_oficial`, `justificativa`) preenchidos como `None`. Estes "espaços em branco" são o gatilho para o processamento da Inteligência Artificial.
3. **Idempotência (Upsert):** Utilizamos a função `.upsert()` do Supabase baseada no ID do parlamentar. Isso garante que o script possa ser rodado múltiplas vezes (rotina diária ou semanal) sem duplicar políticos ou discursos no banco de dados.

**Trecho de destaque (Filtro de Ruído):**
```python
def buscar_ultimo_discurso_relevante(id_camara):
    # ... (código de conexão com a API omitido para brevidade) ...
    for discurso in dados:
        texto = discurso.get("transcricao", "")
        data_hora = discurso.get("dataHoraInicio", "2023-01-01T00:00").split("T")[0]

        # Regra de Negócio: Ignora discursos curtos/protocolares
        if len(texto) > 150:
            return texto, data_hora

    return "Nenhum discurso relevante encontrado após aplicar os filtros.", "2023-01-01"
