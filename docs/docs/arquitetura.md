# Arquitetura do Software

Este documento detalha a estrutura técnica do projeto **ContraDito**, descrevendo os padrões de projeto, tecnologias e o fluxo de dados entre os componentes do sistema.

## 1. Visão Geral e Padrão Arquitetural

O projeto utiliza o padrão **Pipe and Filter** (Cano e Filtro) para o seu pipeline de processamento de dados. Nesse modelo, os dados passam por uma série de componentes independentes (filtros) que transformam ou enriquecem a informação antes de passá-la para o próximo estágio.

### 1.1. O Pipeline de Dados do ContraDito:
1.  **Extração (Source):** Scripts de raspagem coletam dados brutos da Câmara dos Deputados.
2.  **Persistência Inicial:** Dados brutos são inseridos no Supabase.
3.  **Processamento de IA (Filtro):** O Ollama processa os discursos, calcula o *score* de coerência e gera as justificativas.
4.  **Enriquecimento (Filtro):** O banco de dados é atualizado com as análises da IA.
5.  **Exibição (Sink):** A API FastAPI serve os dados processados para o Frontend em Next.js.

---

## 2. Tecnologias Utilizadas (Tech Stack)

| Camada | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js | Interface do usuário e visualização de dados. |
| **Backend** | FastAPI (Python) | Fornecimento da API REST e integração com o banco. |
| **Banco de Dados** | Supabase (PostgreSQL) | Armazenamento persistente e Seeding de dados. |
| **Inteligência Artificial** | Ollama / Llama 3 | Processamento de linguagem natural e cálculo de score. |
| **Infraestrutura** | Docker / Docker Compose | Containerização e ambiente de desenvolvimento. |
| **CI/CD** | GitHub Actions | Automação de Linter (Flake8/Black) e Deploy. |

---

## 3. Componentes do Sistema

### 3.1. Backend (API)
Desenvolvido em **FastAPI**, utiliza **Pydantic** para validação de contratos de dados.
* **Rotas Principais:**
    * `GET /politicos`: Listagem com filtros e paginação.
    * `GET /politicos/{id}`: Detalhes completos, score e provas de contradição.
* **Documentação:** Swagger integrado disponível em `/docs`.

### 3.2. Frontend (Interface)
Aplicação em **Next.js** focada em experiência do usuário (UX) e acessibilidade.
* **Busca:** Filtros por partido, estado e cargo.
* **Raio-X do Parlamentar:** Exibição visual do *Score de Coerência* e comparação lado a lado de discursos/votos.

### 3.3. Inteligência Artificial (Análise)
Utiliza o **Ollama** para processamento local de modelos de linguagem (LLM).
* Analisa discursos inseridos no banco.
* Gera *tags* e justifica as contradições detectadas.
* Atualiza o campo `score_coerencia` no banco de dados.

### 3.4. Banco de Dados
Instância no **Supabase** que atua como o ponto central de integração entre o script de extração, a IA e o Backend.

---

## 4. Integração e Deploy

O projeto é totalmente containerizado via **Docker Compose**, permitindo que o Backend e o Frontend subam simultaneamente com um único comando, garantindo a paridade entre os ambientes de desenvolvimento e produção.

* **Linter:** Garantia de qualidade de código via GitHub Actions.
* **Pipeline:** Verificação automática em cada Pull Request para a branch `develop`.