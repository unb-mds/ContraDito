# Sprint 5 - Implementação da Arquitetura Vetorial (RAG)

**Período:** 21/04/2026 a 28/04/2026

## Descrição
Esta Sprint é dedicada à reestruturação técnica do motor de Inteligência Artificial do **ContraDito**, conforme decidido no diagnóstico do dia 20/04. O foco sai da classificação genérica por LLM e entra na **Busca Vetorial de Precisão**, utilizando embeddings de 768 dimensões e a extensão `pgvector` no Supabase para garantir que as contradições sejam detectadas com base em similaridade semântica real.

## Backlog da Sprint
| Tarefa | Responsável | Status |
| :--- | :--- | :--- |
| **Banco e API:** Ativação do `pgvector`, migrations de colunas de embedding e índice HNSW. Refatoração da lógica de consulta. | @henriquemendeselias | [ ] A fazer |
| **ETL e Higienização:** Limpeza de dados com RegEx e integração do gerador de vetores no fluxo de extração. | @jot4-ge | [ ] A fazer |
| **Motor de Embeddings:** Script PoC com `sentence-transformers` (modelo multilingual) e teste de similaridade de cosseno. | @luizhtmoreira | [ ] A fazer |
| **UX/UI Refactor:** Redesenho da interface para o confronto "Projeto vs. Discurso" e adaptação para justificativas da IA. | @G2SBiell | [ ] A fazer |
| **Infra/Docker:** Isolamento de dependências pesadas (PyTorch/SBERT) em contêiner de Worker e setup do banco vetorial local. | @lucasaraujoszz | [ ] A fazer |
| **Documentação:** Redação do ADR 001 e atualização das páginas de Arquitetura e Cálculo do Score. | @matheus0346 | [ ] A fazer |

## Reuniões
### Planejamento da Sprint 05
* **Data:** 21/04/2026 (14:00h)
* **Ata:** Revisamos a falha da Sprint 04 e detalhamos as tarefas técnicas para a virada de chave para o RAG. O time concordou que a prioridade é a estabilização do banco vetorial no Dia 2 da Sprint, Alem disso começamos 
