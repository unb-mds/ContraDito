# ContraDito

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge" alt="Status do Projeto">
  <img src="https://img.shields.io/badge/MDS-UnB%20FGA-blue?style=for-the-badge" alt="Universidade de Brasília">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">
</p>

> **O que foi dito *vs.* O que foi votado.** Uma plataforma de transparência política movida a Inteligência Artificial.

## Sobre o Projeto
O **ContraDito** é um projeto universitário desenvolvido pela **Squad 09** para a disciplina de Métodos de Desenvolvimento de Software da Universidade de Brasília (UnB - FCTE). 

O sistema atua como um portal de transparência que cruza discursos proferidos por parlamentares (extraídos via API de Dados Abertos da Câmara/Senado) com seus respectivos votos em plenário. Utilizando Processamento de Linguagem Natural (LLM), o sistema gera um **Score de Coerência** e exibe "Provas de Contradição", permitindo que o cidadão acompanhe a postura real de seus representantes.

---

## Principais Funcionalidades (MVP)
- **Busca Descomplicada:** Encontre políticos pelo "nome de urna", partido, cargo ou estado.
- **Raio-X do Parlamentar:** Perfil detalhado com o *Score de Coerência* atualizado e tags de postura política.
- **Provas da Contradição:** Tabela comparativa "Lado a Lado" vinculando o discurso à votação oficial.
- **Transparência Absoluta:** Rastreabilidade de dados com links diretos para as fontes oficiais da Câmara.

---

## Arquitetura: Pipe and Filter
O sistema foi desenhado visando total desacoplamento, performance e consistência de dados, operando em um fluxo linear de 5 filtros principais:

1. **Extração:** Script consome os dados brutos da API da Câmara e padroniza metadados (`nome_urna`).
2. **Motor IA:** Modelo de linguagem (Ollama) avalia a coerência texto-voto e gera as *Tags*.
3. **Persistência:** Dados enriquecidos são salvos de forma relacional no **Supabase** (PostgreSQL).
4. **Disponibilização:** O Back-end filtra, pagina e valida os dados.
5. **Visualização:** A interface responsiva consome a API e renderiza as informações para o cidadão.

---

## Tecnologias Utilizadas

* **Back-end:** Python, FastAPI, Pydantic.
* **Banco de Dados:** Supabase (PostgreSQL), Supabase-py.
* **Inteligência Artificial:** Ollama (LLM Local).
* **Infraestrutura:** Docker, Docker Compose, GitHub Actions (CI/Linter).
* **Documentação:** MkDocs.

---

## Como rodar o projeto localmente

### Pré-requisitos
* [Docker](https://www.docker.com/) e Docker Compose instalados.
* Git.

### Passos de Instalação
1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/sua-organizacao/entrelinhas-contradito.git](https://github.com/sua-organizacao/entrelinhas-contradito.git)
   cd entrelinhas-contradito

2. **Configure as Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz do projeto e insira suas credenciais:
   ```env
   SUPABASE_URL=sua_url_do_projeto_aqui
   SUPABASE_KEY=sua_chave_anon_publica_aqui

3. **Suba os containers da aplicação:**

    No terminal, rode o comando:

    ```bash
    docker-compose up --build

4. **Acesse e Teste:**

    Front-end: http://localhost:3000

    Back-end/Docs: http://localhost:8000/docs

## Squad 09

Este projeto foi construído colaborativamente por:

- **Henrique - @henriquemendeselias**
- **João Guilherme - @jot4-ge**
- **Luiz Henrique - @luizhtmoreira**
- **Gabriel - @G2SBiell**
- **Lucas - @lucasaraujoszz**
- **Matheus - @matheus0346**