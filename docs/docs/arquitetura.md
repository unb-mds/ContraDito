# Arquitetura do Software

Este documento detalha a estrutura técnica do projeto **ContraDito**, descrevendo os padrões de projeto, tecnologias e o fluxo de dados entre os componentes.

## 1. Visão Geral e Padrão Arquitetural

O projeto utiliza o padrão **Pipe and Filter** (Cano e Filtro) para o seu pipeline de processamento de dados. Nesse modelo, os dados passam por uma série de filtros que transformam a informação bruta da API da Câmara em uma análise de coerência política.

### 1.1. O Pipeline de Dados Evoluído (RAG):
Após o pivot técnico na Sprint 5, o pipeline foi reestruturado para utilizar **Busca Vetorial (Retrieval-Augmented Generation)**, abandonando o modelo *one-shot*:

1.  **Extração e Higienização:** Scripts coletam dados da Câmara e utilizam **RegEx** para limpar ruídos e tags HTML.
2.  **Vetorização (Embeddings):** O texto limpo é processado pelo modelo **SBERT** (`paraphrase-multilingual-mpnet-base-v2`), gerando vetores de **768 dimensões**.
3.  **Persistência e Busca Vetorial:** Os dados e seus vetores são armazenados no **Supabase** com a extensão **`pgvector`**. O sistema realiza uma busca por **Similaridade de Cosseno** para cruzar leis e discursos.
4.  **Inferência de Postura (Filtro IA):** O Llama 3 recebe apenas o contexto filtrado (Lei + Discurso relevante) para definir a postura (A Favor/Contra) e gerar a justificativa.
5.  **Exibição (Sink):** A API FastAPI serve os resultados processados para o Frontend em Next.js/Streamlit.

---

## 2. Tecnologias Utilizadas (Tech Stack)

| Camada | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js / Streamlit | Interface do usuário e visualização do Score de Coerência. |
| **Backend** | FastAPI (Python) | Fornecimento da API REST e lógica de busca vetorial. |
| **Banco de Dados** | Supabase + `pgvector` | Armazenamento persistente e busca por similaridade semântica (HNSW). |
| **Inteligência Artificial** | SBERT & Llama 3 | Geração de embeddings e inferência de postura via RAG. |
| **Infraestrutura** | Docker / Docker Compose | Containerização e isolamento de dependências pesadas (PyTorch). |

---

## 3. Componentes do Sistema

### 3.1. Backend (API)
Desenvolvido em **FastAPI**, utiliza **Pydantic** para validação de contratos. É responsável por orquestrar a consulta ao banco vetorial e entregar o contexto para a IA.

### 3.2. Inteligência Artificial (Análise Semântica)
O motor de IA foi dividido em duas etapas para evitar a **Sobrecarga Cognitiva** observada em modelos *one-shot*:

* **Embeddings:** Transforma discursos e leis em coordenadas matemáticas.
* **RAG (Llama 3):** Atua apenas na etapa final, interpretando a relação entre os textos recuperados pelo banco.

### 3.3. Banco de Dados e Busca Vetorial
Instância no **Supabase** que utiliza a extensão `pgvector`. A utilização de índices **HNSW** permite que o sistema encontre contradições em milissegundos, cruzando a ementa de um projeto exclusivamente com os discursos do parlamentar que o votou.

---

## 4. Evolução da Arquitetura: Do One-Shot ao RAG

Originalmente, o projeto tentou processar todas as informações em uma única chamada ao LLM (*One-Shot Prompting*). O modelo recebia o texto bruto e deveria classificar o tema, extrair o assunto e definir a postura simultaneamente.

**O Problema Encontrado:**
Ao escalar para 513 deputados, o modelo apresentou alucinações e erros de formatação (JSON quebrado) por não conseguir processar o volume de discursos subjetivos de uma só vez.

**A Solução Adotada:**
Migramos para uma arquitetura de **Recuperação Vetorial**. Agora, o "trabalho pesado" de encontrar o discurso certo para a lei certa é feito matematicamente pelo banco de dados (Busca Vetorial). O LLM é acionado apenas para a análise final, garantindo precisão e eliminando alucinações.

---

## 5. Integração e Deploy

O projeto é totalmente containerizado via **Docker Compose**, com as dependências de IA (PyTorch/Transformers) isoladas para garantir performance na API.

* **Linter:** Garantia de qualidade via GitHub Actions.
* **Pipeline:** Verificação automática em cada Pull Request para a branch `develop`.
