# Banco de Dados e Busca Vetorial (Supabase)

Este documento apresenta a arquitetura de dados que sustenta o Supabase do **ContraDito**. O foco aqui não é o mapeamento estrito de colunas ou tipagens de código, mas sim documentar como o banco de dados atua como um filtro ativo no pipeline RAG (*Retrieval-Augmented Generation*).

---

## 1. Modelo Conceitual de Dados

O banco de dados foi projetado para unir dados relacionais tradicionais com coordenadas espaciais (vetores), dividindo-se em dois domínios principais:

### A. Perfil e Agregação (`politicos`)
Armazena o cadastro governamental oficial e o estado consolidado do parlamentar.

> **Regra de Negócio Central:** O sistema prevê nativamente a ausência de dados. O score de coerência não possui um valor padrão arbitrário (como `0`). Se um parlamentar não tiver histórico de discursos ou votações processadas, a nota agregada será nula (`null`). Isto permite que o Front-end reaja corretamente ao estado de "Sem Dados", evitando acusar falsamente um político de incoerência por mera falta de histórico.

### B. O Núcleo do RAG (`provas_contradicao`)
É o repositório central onde a inteligência semântica opera. Esta estrutura amarra as três pontas do processo de checagem de coerência:
1. **A Evidência Bruta:** O texto literal extraído do discurso (higienizado pelo fluxo de ETL) e a sua respetiva representação em formato de vetor de 768 dimensões.
2. **O Alvo:** A ementa ou assunto do Projeto de Lei/PEC que está sob escrutínio.
3. **O Veredito:** A inferência gerada assincronamente pelo Motor NLP (Llama 3), que preenche as lacunas de postura (ex: "A Favor" / "Contra"), a justificativa do modelo e o status final de coerência derivado do confronto direto com o painel oficial de votação.

---

## 2. O Motor Semântico: `pgvector` e HNSW

O Supabase no ContraDito não opera apenas como um repositório passivo de textos, mas como um **motor de cálculo matemático acelerado**.

* **O Espaço Vetorial (`pgvector`):** Cada discurso processado pelo *Worker* é convertido num vetor matemático. O banco de dados consegue mapear a "assinatura semântica" do texto, agrupando ideias similares (ex: "corte de gastos" e "redução de despesas") independentemente do vocabulário exato utilizado.
* **Índice HNSW (*Hierarchical Navigable Small World*):** Avaliar a similaridade de um texto contra toda a base de dados utilizando busca sequencial (*Full Table Scan*) causaria exaustão de recursos. Para garantir a escalabilidade do sistema, o índice HNSW cria um grafo em camadas que permite à *query* de busca "pular" vetores matematicamente distantes, garantindo cruzamentos semânticos em milissegundos.

---

## 3. A Busca Ativa: Função RPC

A extração de contexto não ocorre na API principal, mas sim dentro do banco de dados através de uma *Stored Procedure* (RPC) chamada `buscar_discursos_similares`. Isto protege o back-end de gargalos de rede e de processamento.

* **Distância de Cosseno (`<=>`):** A função SQL utiliza este operador vetorial para medir o ângulo entre o vetor da busca (ementa da Lei) e os vetores dos discursos do parlamentar alvo. Distâncias menores indicam alta similaridade semântica.
* **Escudo Anti-Alucinação (*Match Threshold*):** A função recebe um parâmetro de corte de precisão rigoroso. Caso o parlamentar alvo nunca se tenha pronunciado sobre o tema pesquisado, as distâncias matemáticas serão altas. A RPC bloqueia esses resultados e retorna vazio. **Este comportamento impede que o LLM receba "ruído" ou textos fora de escopo, mitigando drasticamente o risco de alucinações.**

---

## 4. Contratos de API (FastAPI)

Para evitar a obsolescência da documentação e garantir que a fonte da verdade seja sempre o código vivo, não documentamos estaticamente as tipagens (Pydantic), campos exigidos ou formatos de resposta JSON neste ficheiro.

> **Documentação Viva:** Todos os contratos da API — incluindo validações de entrada, paginação, formatos de erro, tratamento de campos opcionais (nulos) e respostas de busca vetorial — estão mapeados e interativos via **OpenAPI**.

Para integrações, consulte diretamente as rotas `/docs` (Swagger UI) ou `/redoc` do servidor FastAPI em execução para validar os contratos oficiais da aplicação.
