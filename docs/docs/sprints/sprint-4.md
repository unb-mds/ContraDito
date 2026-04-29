# Sprint 4 - Escala, Benchmarking e o Pivot Arquitetural

**Período:** 14/04/2026 a 21/04/2026

## Descrição
A Sprint 04 começou com o objetivo de escalar a base de dados (para os 513 deputados) e aprimorar a interface com base em benchmarking de mercado. No entanto, o aumento da carga de dados expôs limitações críticas na arquitetura inicial da IA. Isso forçou a equipe a realizar um diagnóstico profundo e um *pivot* arquitetural de emergência, mudando a forma como o sistema processa e cruza os dados.

## Benchmarking e UX
A equipe consultou o portal **"Ranking dos Políticos"** para realizar um estudo de usabilidade. O objetivo foi mapear boas práticas de design para a exibição clara do Score de Coerência e inspirar os novos wireframes do Front-end.

## Backlog Original da Sprint (Planejamento)
| Tarefa | Responsável | Status |
| :--- | :--- | :--- |
| **API:** Implementação de ordenação por score e cache nas rotas. | @henriquemendeselias | [x] Concluído |
| **Extração:** Ajuste no script (Seeder) para extrair os 513 deputados e filtrar ruído. | @jot4-ge | [x] Concluído |
| **IA:** *Fine-tuning* do prompt para evitar alucinações. | @luizhtmoreira | [x] Concluído (Gerou o Pivot) |
| **Front-end:** Wireframes das páginas do site. | @G2SBiell | [x] Concluído |
| **Infra:** Manutenção preventiva do docker-compose e script de backup. | @lucasaraujoszz | [x] Concluído |
| **Documentação:** Explicação do cálculo do score de coerência. | @matheus0346 | [x] Concluído |

---

## O Diagnóstico Técnico (O Problema)
Ao tentar aplicar o LLM (Llama 3 8B) operando de forma linear sobre a base completa de 513 deputados, identificamos uma falha crítica:
* **Sobrecarga Cognitiva:** Tentar enquadrar discursos políticos (que são altamente subjetivos e cheios de eufemismos) em categorias temáticas rígidas (ex: Economia, Saúde) forçava o modelo a "adivinhar" o contexto da fala.
* **Inconsistências:** Essa sobrecarga gerava *parse errors* na formatação de saída (JSON) e alucinações na correlação de contexto, tornando a auditoria da coerência política pouco confiável.

## Decisões Arquiteturais (A Solução)
Na reunião extraordinária do dia 20/04, a equipe decidiu abandonar a classificação discreta de tópicos e pivotar para uma arquitetura baseada em **Recuperação Vetorial (RAG)**. 

O projeto manteve a macroarquitetura *Pipe and Filter*, mas os filtros internos de IA foram reestruturados com as seguintes decisões:

1. **Adoção do SBERT (Embeddings):** A classificação de tópicos e a extração de assuntos, que antes eram feitas de uma só vez pelo Llama (*one-shot prompting*), foram substituídas por modelos de similaridade semântica para português (`paraphrase-multilingual-mpnet-base-v2`). Textos de leis e discursos passam a ser transformados em vetores matemáticos (arrays de 768 dimensões) localmente.
2. **Supabase como Banco Vetorial:** Ativação da extensão `pgvector` com índices HNSW. A busca cruza a ementa da lei exclusivamente com os discursos do parlamentar que votou, via matemática pura (Similaridade de Cosseno), eliminando falsos positivos.
3. **Redução do Escopo do LLM:** O Llama 3 deixa de atuar como classificador de temas. Ele passa a receber o par exato selecionado pela busca vetorial (Lei + Discurso), focando 100% de sua capacidade em inferir a intenção e a postura (A FAVOR, CONTRA, NEUTRO).

---

## Reuniões

### 1. Planejamento da Sprint 04
* **Data:** 14/04/2026
* **Ata:** Definição do escopo de escala para 513 deputados, estudo de benchmarking ("Ranking dos Políticos") e delegação das frentes de trabalho.

### 2. Reunião Extraordinária (Pivot Arquitetural)
* **Data:** 20/04/2026
* **Ata:** Reunião emergencial focada em diagnosticar os erros do Llama 3. A equipe oficializou a transição para a Busca Vetorial descrita acima, com as tarefas de refatoração do banco e dos scripts movidas diretamente para o Backlog da Sprint 05.
