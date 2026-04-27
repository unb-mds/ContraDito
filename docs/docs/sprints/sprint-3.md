# Sprint 3 - Desenvolvimento do MVP e Fluxo de Dados

**Período:** 07/04/2026 a 14/04/2026

## Descrição
Com o esqueleto arquitetural validado na Sprint anterior, a Sprint 03 teve como foco o desenvolvimento principal do Produto Mínimo Viável (MVP). O objetivo foi aplicar o padrão *Pipe and Filter* na prática: automatizar a extração dos dados (seeding), rodar a Inteligência Artificial em lote para calcular o Score de Coerência e expor essas informações através de rotas consumidas por um Front-end funcional.

## Objetivos e Requisitos do MVP
Durante a reunião de planejamento, a equipe fechou o escopo dos requisitos essenciais a serem entregues:

* **Descoberta:** Barra de busca global (incluindo o "nome de urna" oficial) e filtros de listagem por Partido, Cargo e Estado.
* **Raio-X do Parlamentar:** Tela de perfil exibindo o *Score de Coerência* visual e as *Tags* de postura.
* **Provas da Contradição:** Tabela de comparação direta (O que foi dito *vs.* O que foi votado).
* **Transparência:**

url câmara: https://dadosabertos.camara.leg.br/api/v2

url senado: https://legis.senado.leg.br/dadosabertos

## Backlog e Responsabilidades
| Tarefa | Responsável | Status |
| :--- | :--- | :--- |
| **API Backend:** Atualização de Pydantic/Supabase (Contrato) e implementação das rotas GET `/politicos` (com paginação/filtros) e `/politicos/{id}`. | @henriquemendeselias | [x] Concluído |
| **Integração de Dados:** Carga inicial automatizada (Seeding de 20-50 deputados) com `id_parlamentar` oficial para linkagem. | @jot4-ge | [x] Concluído |
| **Inteligência Artificial:** Processamento local em lote (Ollama) das amostras, cálculo do score e geração de justificativas com UPDATE no banco. | @luizhtmoreira | [x] Concluído |
| **Front-end:** Setup (Next.js), criação da tela de busca, filtros e consumo da API para montar o "Raio-X do Parlamentar". | @G2SBiell | [x] Concluído |
| **Infraestrutura:** Docker-compose simultâneo (FastAPI + Front) e automação de Linter (Flake8/Black) no GitHub Actions para os PRs. | @lucasaraujoszz | [x] Concluído |
| **Documentação:** Criação das páginas de Arquitetura (Pipe and Filter) e LGPD/Cálculo do Score no MkDocs. | @matheus0346 | [x] Concluído |

## Cronograma de Execução (6 Dias)
Para garantir que as dependências não bloqueassem o time, o Scrum Master estabeleceu a seguinte esteira de execução:

* **Dias 1-2:** O Contrato de API (JSON) foi selado; Banco atualizado e a carga inicial de deputados foi realizada no Supabase.
* **Dias 3-4:** A IA processou os deputados inseridos no banco; O Front-end iniciou o consumo da busca com base no contrato estabelecido.
* **Dia 5:** Integração final — validação do clique da busca para a abertura do perfil com o score real.
* **Dia 6:** Finalização do Docker para demonstração e polimento da documentação no MkDocs.

## Reuniões

### Ata de Reunião (Planejamento da Sprint 03)
* **Data:** 07/04/2026
* **Participantes:** Henrique, João, Luiz, Gabriel, Lucas e Matheus.
* **Decisões Principais:** Formalização da arquitetura *Pipe and Filter* e priorização do contrato de API logo no Dia 1, mitigando o risco de retrabalho entre as frentes de Backend, IA e Frontend.
