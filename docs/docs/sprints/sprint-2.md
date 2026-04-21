# Sprint 2 - O "Walking Skeleton" e Validação de Hipóteses

**Período:** 02/04/2026 a 07/04/2026

## Descrição
A Sprint 02 focou na construção do "Walking Skeleton" do ContraDito. O objetivo foi validar as hipóteses técnicas e garantir que as diferentes frentes (Extração, IA, Backend e Frontend) conseguissem se comunicar. Em vez de funcionalidades completas, priorizamos a integração: um dado real da Câmara fluindo pelo motor de NLP e sendo visualizado em um protótipo, tudo dentro de um ambiente Dockerizado.

## Definições Tecnológicas (Stack Oficial)
Durante esta sprint, o time fechou o conjunto de ferramentas que sustentará o projeto:

| Frente | Tecnologia Definida |
| :--- | :--- |
| **Backend / API** | FastAPI & Supabase |
| **Pipeline Interno** | Apache Airflow & Playwright |
| **Motor NLP (IA)** | LangChain, spaCy & Transformers (Hugging Face) |
| **Front-End** | Streamlit & Tailwind CSS |

## Backlog da Sprint
As tarefas foram desenhadas com foco em "Pontes de Integração":

| Tarefa | Responsável | Status |
| :--- | :--- | :--- |
| Extração de amostras reais (.json) e desenho do DER | @jot4-ge | [x] Concluído |
| Script PoC (Ollama) validado com dados reais | @luizhtmoreira | [x] Concluído |
| Setup FastAPI, Supabase e Contrato de API | @henriquemendeselias | [x] Concluído |
| Protótipo de Média Fidelidade (Figma) | @G2SBiell | [x] Concluído |
| Docker-compose enxuto e regras de branch/commit | @lucasaraujoszz | [x] Concluído |
| Setup do MkDocs e registro das "Regras do Jogo" | @matheus0346 | [x] Concluído |

## Reuniões

### Ata de Reunião Extraordinária (Planejamento)
* **Data:** 02/04/2026
* **Horário:** 18:00 às 18:45
* **Local:** google meet
* **Participantes:** @henriquemendeselias, @jot4-ge, @luizhtmoreira, @matheus0346, @lucasaraujoszz, @G2SBiell.
* **Decisões:** 1. Definição da stack tecnológica completa (FastAPI, Airflow, LangChain, Streamlit).
    2. Acordo de que nenhum código de integração seria feito sem a definição prévia do **Contrato de API** entre Backend e Frontend.
    3. Implementação imediata de travas na branch `main` para garantir a qualidade via Pull Requests.

## Finalização
A Sprint 02 permitiu que o time saísse do campo teórico para o prático. Com o ambiente Docker configurado e as amostras reais de discursos validadas pela IA, o esqueleto do projeto está pronto para receber as funcionalidades de busca e visualização de scores na próxima etapa.
