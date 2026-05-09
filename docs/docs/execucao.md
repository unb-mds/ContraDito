# Manual de Execução: Infraestrutura Local

Este documento detalha o processo de provisionamento do ambiente de desenvolvimento do **ContraDito**. A infraestrutura foi desenhada para ser previsível, leve e replicável através de contêineres, garantindo uma execução à prova de falhas em qualquer sistema operacional (incluindo suporte nativo para arquiteturas ARM64 e AMD64).

---

## 1. Visão Geral dos Contêineres

A orquestração do nosso ambiente é feita inteiramente via **Docker Compose**, que sobe 4 contêineres simultâneos e interligados:

* 📦 **`banco_dados-1`**: Banco PostgreSQL local com extensão `pgvector` ativada (porta `5432`).
* 📦 **`api-1`**: API Principal em FastAPI. Atua como o "garçom" do sistema, respondendo ao Front-end (porta `8000`).
* 📦 **`worker-1`**: Worker isolado de IA em FastAPI. Vive "enclausurado" na rede do Docker por questões de segurança e processamento de NLP (porta interna `8001`).
* 📦 **`frontend-1`**: Interface da aplicação desenvolvida em Next.js (porta `3000`).

---

## 2. Passo a Passo para Execução Local

### Passo 1: Clonar o Repositório
Certifique-se de estar na branch `develop` do repositório oficial.
```bash
git clone [https://github.com/SeuUsuario/ContraDito.git](https://github.com/SeuUsuario/ContraDito.git)
cd ContraDito
git checkout develop
```

### Passo 2: Configurar as Variáveis de Ambiente
Para que os contêineres se comuniquem corretamente, crie um arquivo chamado `.env` na raiz do projeto (mesmo nível do `docker-compose.yml`) com o conteúdo abaixo:

```env
# Banco de Dados (Ambiente Local Docker)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=contradito

# Integração Supabase (Caso vá testar o banco em Nuvem)
SUPABASE_URL=sua_url_do_supabase_aqui
SUPABASE_KEY=sua_chave_anon_aqui

# Comunicação Interna da API com a IA (Docker Bridge)
WORKER_URL=http://worker-1:8001

# Variáveis do Front-end (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
WATCHPACK_POLLING=true
```

### Passo 3: Subir a Infraestrutura
Com o Docker em execução na sua máquina, abra o terminal na raiz do projeto e rode o comando de orquestração:

```bash
docker compose up --build
```

**E pronto!** O Docker fará o download das dependências (aproveitando a técnica de *Layer Caching* para otimização de velocidade) e levantará o sistema. 

Você poderá acessar:

* **Interface do Usuário:** `http://localhost:3000`
* **Documentação da API (Swagger):** `http://localhost:8000/docs`

> **Dica de Desenvolvimento (DX):** O ambiente possui *Hot-Reload* nativo mapeado por volumes. Qualquer alteração no seu editor de código refletirá instantaneamente na aplicação. Para derrubar o ambiente limpando as redes residuais, utilize o comando `docker compose down`.

---

## 3. Entendendo o Isolamento Arquitetural (API vs. Worker IA)

Uma das decisões arquiteturais mais importantes do ContraDito para garantir performance foi a separação física do tráfego web do processamento de Inteligência Artificial.

* **O Roteador (`api-1`):** É leve, foca em consultas ao banco e entrega de dados ao front-end. Possui **cache em memória** para otimizar requisições repetidas.
* **O Motor Pesado (`worker-1`):** Dedicado exclusivamente a carregar o modelo de embedding (SBERT) na memória para vetorização. No nosso `docker-compose.yml`, o Worker não possui mapeamento de portas para a máquina hospedeira. Ele recebe ordens apenas da API Principal. Isso garante que, caso a carga da IA estoure a memória da máquina, o contêiner principal (`api-1`) continua no ar, retornando falhas tratadas para o usuário sem derrubar a aplicação por completo.
