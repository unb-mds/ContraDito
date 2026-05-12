# Integração e API (Rotas e Swagger)

A API do ContraDito foi construída utilizando **FastAPI**, com foco em alta performance, respostas cacheadas e processamento assíncrono para as rotas de Inteligência Artificial.

---

## 1. Documentação Interativa (Swagger)

Toda a documentação dos *schemas* (modelos de dados), contratos de requisição e testes de rotas é gerada automaticamente pelo FastAPI.

Com os containers em execução, acesse:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Local / Desenvolvimento:** `http://localhost:8000`


---

# 2. Domínio: Políticos (`/api/politicos`)

Este módulo é responsável pelo consumo principal do Front-end, alimentando tanto a listagem de parlamentares quanto a página individual do político.

---

## 2.1. Listar e Filtrar Políticos

### `GET /api/politicos`

Retorna uma listagem paginada de parlamentares.

A rota utiliza **cache em memória de 1 hora (`3600s`)**, reduzindo consultas repetidas e garantindo carregamento rápido da página inicial.

### Parâmetros de Query (Filtros Opcionais)

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `busca` | `string` | Pesquisa parcial por nome de urna |
| `partido` | `string` | Partido político (`PT`, `PL`, etc.) |
| `cargo` | `string` | Cargo parlamentar (`DEPUTADO`, `SENADOR`) |
| `uf` | `string` | Unidade federativa (`SP`, `RJ`) |
| `ordem` | `string` | `mais_coerentes` ou `menos_coerentes` |
| `pagina` | `int` | Página atual da paginação |


### Retorno de Sucesso (`200 OK`)

```json
{
  "total_registros": 513,
  "pagina_atual": 1,
  "tamanho_pagina": 20,
  "total_paginas": 26,
  "itens": [
    {
      "id": 1,
      "nome_urna": "Fulano",
      "score_coerencia": 85.5,
      "uf": "SP"
    }
  ]
}
```

---

## 2.2. Obter Perfil Detalhado

### `GET /api/politicos/{id_parlamentar}`

Rota consumida na tela individual do parlamentar.

Retorna os dados cadastrais do político juntamente com todo o histórico de análises semânticas e provas de contradição vinculadas ao parlamentar.

### Retorno de Sucesso (`200 OK`)

```json
{
  "politico": {
    "id": 1,
    "nome_urna": "Fulano",
    "cargo": "DEPUTADO",
    "score_coerencia": 85.5
  },
  "provas": [
    {
      "id": 10,
      "contexto": {
        "tipo_documento": "DISCURSO",
        "data_evento": "2024-05-10",
        "texto_extraido": "Sempre fui a favor do teto de gastos..."
      },
      "resultado": {
        "topico_identificado": "Economia",
        "postura_extraida_do_texto": "A Favor",
        "justificativa": "O parlamentar defende explicitamente o limite.",
        "voto_oficial_registrado": "Contra",
        "status_coerencia": false
      }
    }
  ]
}
```

### Tratamento de Erros

| Status Code | Cenário |
|---|---|
| `404 Not Found` | `id_parlamentar` não encontrado no banco de dados |

---

# 3. Domínio: Inteligência Artificial (`/api/politicos/buscar-similares`)

## `POST /api/politicos/buscar-similares`

Esta rota representa o núcleo de Busca Semântica do sistema (**RAG**).

Ao invés de executar processamento NLP diretamente no servidor principal, a API delega a geração de embeddings para um *Worker* assíncrono especializado.

---

## Fluxo de Execução

1. A API recebe o `texto_busca` enviado pelo cliente;
2. O FastAPI realiza uma requisição interna via `httpx` para o container Worker (`http://worker:8001/gerar-embedding`);
3. O Worker NLP gera e devolve o `embedding`;
4. A API executa a RPC `buscar_discursos_similares` no Supabase utilizando o vetor retornado;
5. O banco devolve os discursos semanticamente relacionados.

---

## Corpo da Requisição (Payload)

```json
{
  "texto_busca": "Aumento do limite de gastos governamentais",
  "id_parlamentar": 1,
  "limite": 5
}
```

---

## Retorno de Sucesso (`200 OK`)

Retorna uma lista contendo os discursos que superaram o limiar mínimo de similaridade (*threshold*), ordenados da maior para a menor proximidade semântica.

```json
[
  {
    "id": 45,
    "texto_extraido": "Meu voto sempre foi favorável ao teto...",
    "similaridade": 0.85
  },
  {
    "id": 102,
    "texto_extraido": "É preciso responsabilidade fiscal...",
    "similaridade": 0.78
  }
]
```

---

## Tratamento de Erros

| Status Code | Cenário |
|---|---|
| `400 Bad Request` | Falha na geração do embedding pelo Worker NLP |
| `503 Service Unavailable` | Worker NLP offline ou timeout superior a 15 segundos |

---