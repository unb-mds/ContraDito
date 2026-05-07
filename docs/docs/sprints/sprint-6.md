# Sprint 06: Organização, Planejamento e Documentação

**Projeto:** ContraDito  
**Data da Reunião:** 28/04/2026  
**Data de Entrega da Sprint:** 06/05/2026  

---

## 1. Descrição e Objetivo da Sprint
Realizada a retrospectiva da Sprint 05 e o planejamento focado para a Sprint 06. A nova sprint será dedicada exclusivamente à incrementação dos requisitos, ajustes de planejamento, design no Figma, revisão do README e orquestração da documentação no MkDocs.

**Objetivo Central:** Sprint sem código. Preparar o terreno, direcionar o trabalho de forma inteligente e garantir o alinhamento documental (blindagem jurídica e especificações técnicas) necessário para seguir com o projeto de forma segura para a Release 1.

---

## 2. Participantes
* @henriquemendeselias
* @jot4-ge
* @luizhtmoreira
* @G2SBiell
* @lucasaraujoszz
* @matheus0346

---

## 3. Backlog e Distribuição de Tarefas

| Membro | Missão Principal | Ações e Documentação |
| :--- | :--- | :--- |
| **Henrique** | Consolidar contratos de API e banco. | Atualizar o README. Liderar reunião de validação linha por linha (RFs e RNFs). Revisar Swagger/ReDoc. Criar dicionário de dados do Supabase (tabelas, `provas_contradicao` com tipo vector, tipagens, HNSW e RPC). |
| **Luiz Henrique** | Documentar o "cérebro semântico" (NLP). | Definir requisitos de RAG/embedding. Escrever arquitetura NLP, justificar o uso do SBERT (`paraphrase-multilingual-mpnet`), explicar a matemática da similaridade de cosseno e o limiar (threshold). |
| **João Guilherme** | Mapear o Ciclo de Vida do Dado (ETL). | Checar coleta de vídeos, PDFs, separação de matérias (PEC/PL). Registrar rotas do Governo, explicar regras do `cleaner.py` e definir a rotina de carga delta semanal. |
| **Lucas** | Garantir ambiente replicável (DevOps). | Criar passo a passo local (Worker vs API). Documentar `docker-compose.yml`, variáveis `.env`, separação do FastAPI vs Worker NLP, arquitetura ARM64 vs AMD64 e uso de cache. |
| **Matheus** | Orquestrar MkDocs e blindagem jurídica. | Estruturar menu do MkDocs. Escrever páginas para o cidadão (LGPD, Isenção de Viés) e compilar os ADRs (escolhas de Supabase, isolamento de Worker e pivot para RAG). |
| **Gabriel** | Sincronizar UI/UX e código frontend. | Criar Story Map. Atualizar Figma com nova view "Lado a Lado". Documentar stack do Front (Next.js/Tailwind). Finalizar protótipos de busca, ranking, e ringue face-to-face. |
