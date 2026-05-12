# Arquitetura do Software

## 1. Visão Geral e Padrão Arquitetural

O projeto utiliza o padrão **Pipe and Filter** para o seu pipeline de processamento de dados. Nesse modelo, os dados passam por uma série de filtros que transformam a informação bruta da API da Câmara em uma análise de coerência política.

### 1.1. Pipeline de Dados e Arquitetura Assíncrona (RAG)

O pipeline do ContraDito foi projetado utilizando a abordagem de **Retrieval-Augmented Generation (RAG)**, substituindo o modelo *zero-shot* tradicional e adotando uma arquitetura assíncrona voltada para escalabilidade, isolamento de carga e alta performance.

O fluxo operacional ocorre em cinco etapas principais:

- **Extração e Higienização:** Scripts de ETL realizam a coleta de dados oficiais da Câmara dos Deputados e executam processos de limpeza utilizando RegEx, removendo ruídos textuais, quebras de linha, caracteres inválidos e tags HTML dos discursos originais.

- **Delegação para o Worker NLP (Vetorização):** Para evitar sobrecarga na API principal, a geração de embeddings é delegada a um serviço isolado(Worker NLP). O texto higienizado é processado pelo modelo SBERT `paraphrase-multilingual-mpnet-base-v2`, responsável por gerar embeddings vetoriais de 768 dimensões.

- **Persistência e Busca Vetorial (`pgvector`):** Os dados processados e seus embeddings são armazenados no Supabase/PostgreSQL utilizando a extensão `pgvector`. Durante a análise, o banco executa uma *Stored Procedure* baseada em Similaridade por Cosseno para cruzar semanticamente a ementa da proposição com discursos previamente registrados, retornando apenas os contextos semanticamente relevantes.

- **Inferência de Postura (Worker Llama 3):** Em segundo plano, o Worker injeta o contexto filtrado (ementa + discurso relevante) no modelo Llama 3. O modelo realiza a inferência da `postura_extraida` (`A Favor` ou `Contra`) e produz a justificativa textual que fundamenta a análise de coerência ou contradição.

- **Consumo e Exibição (FastAPI → Next.js):** A API principal atua como camada de orquestração entre Front-end, banco de dados e Workers NLP. O Front-end em Next.js consome rotas cacheadas do FastAPI, responsáveis por servir os resultados consolidados, evidências semânticas e scores finais de coerência com baixa latência.

> **Nota visual:** O modelo de arquitetura pode ser visualizado no link: 
[Figma](https://www.figma.com/board/J6igyv5zX16YPhLaoKM3c4/ContraDito?node-id=0-1&t=Jq1ENqM8V4La6slk-0)
---

## 2. Tecnologias Utilizadas (Tech Stack)

| Camada | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js / Streamlit | Interface do usuário e visualização do Score de Coerência. |
| **Backend** | FastAPI (Python) | Fornecimento da API REST e lógica de busca vetorial. |
| **Banco de Dados** | Supabase + `pgvector` | Armazenamento persistente e busca por similaridade semântica (HNSW). |
| **Inteligência Artificial** | SBERT & Llama 3 | Geração de embeddings e inferência de postura via RAG. |
| **Infraestrutura** | Docker / Docker Compose | Containerização e isolamento de dependências pesadas (PyTorch). |

