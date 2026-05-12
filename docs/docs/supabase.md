# Banco de Dados e Busca Vetorial (Supabase)

## 1. Modelo Conceitual de Dados
O banco de dados foi projetado para unir dados relacionais tradicionais com coordenadas espaciais (vetores), dividindo-se em dois domínios principais:

### 1.1. Perfil e Agregação (`politicos`)

Armazena o cadastro governamental oficial - dados extraídos das APIs: `id`, `nome_civil`, `nome_urna`, `cargo`, `partido`, `UF`, `foto_url` e `situacao`, além do `score_coerencia` após o seu cálculo. Adicionalmente, esta tabela atua como entidade principal no banco de dados, fornecendo a chave estrangeira para a tabela `provas_contradicao`.

O `score_coerencia` deve ser nulo (`null`) caso não haja histórico processado do parlamentar. Isso é essencial para que o Front-end exiba o estado **"Sem Dados"**, em vez de assumir o valor `0` e acusar falsamente o político de incoerência.

### 1.2. O Núcleo do RAG (`provas_contradicao`)

É o repositório central onde a inteligência semântica opera. Esta estrutura conecta as informações essenciais do processo de checagem de coerência:

- **Conteúdo Processado e Rastreabilidade:** Armazena o texto literal do discurso (higienizado pelo fluxo de ETL), acompanhado do seu respectivo `embedding` (vetor utilizado para busca semântica). Cada registro possui um `hash` único para evitar duplicação no banco e mantém metadados de origem, como `tipo_documento`, `data_evento` e `link_fonte`.

- **Contexto Legislativo e Voto Oficial:** Mantém a ementa ou assunto da proposição analisada e registra diretamente o `voto_oficial`, permitindo o cruzamento entre discurso público e posicionamento formal em votações.

- **Inferência do Motor NLP e Veredito:** Armazena a análise gerada de forma assíncrona pelo modelo de IA (Llama 3), responsável por identificar a `postura_extraida` (ex.: `"A Favor"` ou `"Contra"`) e produzir a justificativa textual da inferência. A partir disso, o sistema consolida o `status_coerencia`, um valor booleano derivado da comparação entre `voto_oficial` e `postura_extraida`.

---

## 2. O Motor Semântico: `pgvector` e HNSW

O banco de dados (Supabase/PostgreSQL) do projeto não atua apenas como um repositório passivo de textos, mas também como um mecanismo ativo de busca semântica.

- **Espaço Vetorial (`pgvector`):** Cada discurso processado é convertido em um vetor matemático de 768 dimensões, denominado `embedding`. Esses vetores são armazenados no banco de dados e comparados por meio da métrica de **Similaridade por Cosseno**, utilizada para medir a proximidade semântica entre conteúdos. Essa abordagem permite ao sistema compreender relações de significado entre expressões diferentes — como “corte de gastos” e “redução de despesas” — sem depender de correspondência literal de palavras.

- **Busca Vetorial Otimizada (Índice HNSW):** Comparar um vetor com todos os registros da base tornaria a consulta inviável em escala. Para solucionar esse problema, o sistema utiliza o índice **HNSW** (*Hierarchical Navigable Small World*), responsável por organizar os vetores em uma estrutura hierárquica de vizinhança. Dessa forma, o mecanismo de busca consegue ignorar rapidamente regiões semanticamente irrelevantes e direcionar a consulta apenas aos grupos mais próximos do contexto pesquisado. Isso garante buscas semânticas de alta performance e baixa latência, mesmo com o crescimento contínuo da base de dados.

---

## 3. A Busca Ativa: Função RPC

A extração de contexto utilizada pela inteligência artificial ocorre diretamente no banco de dados por meio de uma *Stored Procedure* (RPC). Executar a busca vetorial próximo aos dados reduz latência, elimina gargalos de rede e garante respostas em escala de milissegundos. A estrutura da função é baseada em quatro pilares principais:

- **Filtro de Escopo (`p_politico_id`):** Antes da execução do cálculo vetorial, a função restringe os registros ao parlamentar alvo, garantindo isolamento contextual e impedindo que discursos de políticos diferentes sejam misturados na análise.

- **Cálculo de Similaridade:** O banco utiliza o operador de **Distância do Cosseno** (`<=>`) para medir proximidade entre embeddings. Como distâncias menores representam maior similaridade semântica, a função aplica a transformação `1 - distância`, produzindo um `score_similaridade` mais intuitivo, no qual valores maiores indicam maior proximidade de significado.

- **Escudo Anti-Alucinação (`match_threshold`):** A similaridade calculada deve obrigatoriamente superar o limite definido em `match_threshold`. Caso o parlamentar não possua discursos semanticamente relacionados ao tema pesquisado, os registros são descartados e a função retorna vazio. Esse mecanismo reduz ruído contextual e mitiga significativamente o risco de inferências imprecisas pelo modelo LLM (Llama 3).

- **Contexto Enxuto (`match_count`):** Para respeitar a janela de contexto do modelo e otimizar o consumo de tokens, os resultados aprovados são ordenados do maior para o menor `score_similaridade` e limitados à quantidade especificada em `match_count`.

#### Retorno para o Back-end

A função retorna apenas os elementos necessários para a composição do prompt enviado ao modelo de IA:

- `id` da evidência;
- `texto_extraido` correspondente ao discurso;
- `score_similaridade` calculado na busca vetorial.
