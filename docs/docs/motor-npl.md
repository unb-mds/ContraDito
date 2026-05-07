# Especificação Técnica: Motor NLP e Pipeline RAG

**Responsável:** Luiz Moreira (@luizhtmoreira)

O motor NLP do projeto **contraDito** opera sob o padrão arquitetural **Pipe and Filter**, onde o processamento de dados é decomposto em etapas independentes e modulares. O objetivo central é transformar textos brutos (discursos e ementas) em vereditos estruturados de coerência política, utilizando uma arquitetura de *Retrieval-Augmented Generation* (RAG).

---

## 1. Visão Geral do Fluxo (Pipeline Pipe and Filter)

O fluxo segue a seguinte sequência lógica:

1.  **Ingestão e Sanitização:** Recebimento dos dados do ETL e limpeza de ruídos (notas taquigráficas, tags HTML).
2.  **Processamento de Texto (Chunking e Resumos):** Adaptação de textos longos aos limites do modelo, dividindo discursos e sumarizando matérias legislativas.
3.  **Vetorização (Embedding):** Conversão de texto em representações matemáticas densas.
4.  **Persistência Vetorial:** Armazenamento de vetores no Supabase utilizando a extensão `pgvector`.
5.  **Busca Semântica (Retrieval):** Recuperação dos trechos de discursos contextualmente mais relevantes à matéria votada.
6.  **Orquestração e Inferência (Generation):** Processamento via LangChain e Llama 3 (LoRA Fine-tuned).
7.  **Cálculo e Persistência de Veredito:** Comparação lógica entre intenção inferida e voto real.

---

## 2. Estratégia de Processamento: Fragmentação e Representação Holística

Modelos de linguagem baseados na arquitetura Transformer possuem um limite estrito de comprimento de sequência (geralmente de 512 tokens para o modelo SBERT escolhido). Como os textos governamentais frequentemente ultrapassam essa marca, o sistema adota duas abordagens distintas para lidar com a volumetria sem perder contexto:

### 2.1. Discursos Parlamentares (Fragmentação Local / Chunking)
Para evitar o truncamento silencioso (onde a IA ignora o final do discurso), o sistema implementa a técnica de *Chunking*:
* **Divisão de Texto:** Discursos completos são fatiados em múltiplos fragmentos utilizando o `RecursiveCharacterTextSplitter` do LangChain.
* **Sobreposição (Overlap):** Cada fragmento preserva uma percentagem de caracteres do trecho anterior. Isso garante que frases que fazem a transição entre ideias não percam o contexto legislativo.
* **Impacto Estrutural:** A relação de persistência evolui de `1 Discurso : 1 Vetor` para `1 Discurso : N Fragmentos Vetorizados`. Na etapa de RAG, o LLM recebe apenas o trecho exato onde a matéria foi debatida, otimizando o consumo de tokens.

### 2.2. Matérias Legislativas (Representação Holística)
Diferente dos discursos, os parlamentares votam no mérito do projeto como um todo (PL/PEC). Fragmentar um Projeto de Lei de 50 páginas e buscar semelhança apenas no primeiro fragmento destruiria a semântica da busca.
* **Âncora Semântica (Ementa):** O sistema prioriza a vetorização da **Ementa** (resumo oficial). Ela é densa, curta, raramente excede os limites de tokens e contém a intenção central da votação.
* **Resumo Global (Fallback):** Caso a ementa seja vaga ou insuficiente, o pipeline utiliza um LLM para gerar um Resumo Executivo Global da matéria antes da vetorização.
* **Impacto Estrutural:** Garante que o "todo" da matéria legislativa seja comparado aos fragmentos (*chunks*) dos discursos, preservando o espírito da lei num único espaço semântico de alta qualidade.

---

## 3. O "Dicionário Semântico": Justificativa do Modelo de Embedding

Para que o sistema compreenda a semântica política brasileira, foi selecionado o modelo **`paraphrase-multilingual-mpnet-base-v2`** (via SBERT).

**Porquê este modelo?**
* **Acurácia Multilíngue:** Treinado especificamente para lidar com múltiplos idiomas, incluindo o Português Brasileiro, capturando nuances e gírias do ambiente legislativo.
* **Arquitetura MPNet:** Combina os benefícios de *Masked Language Modeling* (MLM) e *Permuted Language Modeling* (PLM), resultando em embeddings de 768 dimensões com extrema riqueza semântica.
* **Foco em Paráfrases:** Otimizado para identificar quando dois textos dizem a mesma coisa com palavras diferentes, essencial para correlacionar o linguajar formal e jurídico de uma PEC com o discurso retórico e inflamado de um parlamentar.

---

## 4. A Matemática da Similaridade: Distância de Cosseno

A recuperação de discursos relevantes no banco de dados vetorial não utiliza busca por palavras-chave, mas sim proximidade geométrica.

A métrica principal é a **Similaridade de Cosseno**, que mede o cosseno do ângulo entre dois vetores no espaço n-dimensional. Diferente da distância euclidiana, ela ignora a magnitude (tamanho do texto) e foca apenas na direção (conteúdo semântico).

A fórmula para o cálculo da Similaridade de Cosseno é definida como:

$$Similaridade(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

No Supabase, o cálculo é operado pela **Distância de Cosseno**, onde:

$$Distância = 1 - Similaridade$$

* **Distância próxima de 0:** Textos altamente correlacionados semanticamente.
* **Distância próxima de 1:** Textos sem relação aparente.

---

## 5. O Coração da Inferência: Llama 3 e Fine-Tuning com LoRA

A decisão final sobre a postura do parlamentar é tomada pelo modelo **Llama 3**. Para garantir que o modelo atue como um analista político preciso, aplica-se a técnica de **LoRA (Low-Rank Adaptation)**.

O LoRA permite injetar conhecimento do domínio legislativo brasileiro no Llama 3, treinando apenas uma pequena fração dos parâmetros (matrizes de adaptação). Os benefícios incluem:
* **Especialização:** Adequação ao formato de textos de PLs, PECs e discursos oficiais.
* **Estruturação de Saída:** Garantia de que a resposta seja gerada obrigatoriamente em formato JSON estruturado, evitando falhas de *parsing* na API principal.
* **Economia Computacional:** Redução drástica na memória de GPU necessária.

---

## 6. Orquestração via LangChain

O **LangChain** atua como o framework orquestrador do pipeline, responsável por:
* **Gerenciamento de Prompts:** Injetar dinamicamente a Ementa da votação e os fragmentos de discursos recuperados (*top-k chunks*).
* **Cadeias de Processamento (Chains):** Executar a sequência lógica rígida: *Recuperar -> Formatar -> Analisar -> Justificar*.
* **Controle de Limites:** Filtrar os fragmentos recuperados para garantir que o *prompt* montado não exceda o limite de contexto (*Context Window*) do Llama 3.

---

## 7. Limiar de Similaridade (Threshold) e Validação Empírica

O sistema estabelece um **limiar base de 0.2 de distância de cosseno** para aprovar a relevância de um fragmento de discurso. Se nenhum fragmento atingir este limiar, o modelo LLM não é acionado, evitando inferências baseadas em "alucinações" e poupando processamento.

> **Estratégia de Ajuste Dinâmico:** Este valor de threshold será rigorosamente ajustado durante a fase de validação. Testes empíricos e métricas de *Precision/Recall* serão aplicados contra dados históricos reais para encontrar a linha de corte exata.

---

## 8. Regras de Integridade: O Viés Temporal

Para sustentar a ética analítica do Score de Coerência, o motor NLP impõe um filtro restritivo temporal inquebrável: **Nenhum discurso proferido após a data da votação será considerado pelo cálculo de RAG.** Isto blinda o sistema contra o viés de dados do futuro, julgando o parlamentar exclusivamente pelas convicções públicas que ele possuía no exato momento da votação.

---

### Resumo de Componentes Técnicos

| Componente | Tecnologia | Função |
| :--- | :--- | :--- |
| **Embeddings** | SBERT (mpnet-base-v2) | Transformação de textos em tensores matemáticos. |
| **Processamento de Textos** | LangChain / LLM | Fragmentação (*Chunking*) de discursos e sumarização de matérias. |
| **Vector DB** | Supabase (`pgvector`) | Armazenamento e busca vetorial por Distância de Cosseno. |
| **Orquestrador** | LangChain | Interligação do fluxo RAG e montagem de prompts de inferência. |
| **LLM** | Llama 3 + LoRA | Decisão de postura política e justificativa textual formatada. |
| **Formato de Saída** | JSON | Contrato rigoroso para facilitação da integração do backend. |
