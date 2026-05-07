# Escopo e Visão Geral do Produto

Para garantir a entrega de um Produto Mínimo Viável (MVP) funcional, testável e de alto valor agregado dentro do semestre letivo, o **ContraDito** delimitou um escopo de atuação rigoroso.

## 1. Visão Geral
O sistema funciona como um "motor de auditoria contínua". Ele coleta o histórico legislativo (fala e voto) de políticos, processa o texto semanticamente através de Inteligência Artificial e exibe um **Score de Coerência** ao eleitor. 

A interface central do produto é o **Ringue Face-to-Face**, onde a tela se divide: de um lado, o que o parlamentar discursou em plenário; do outro, como ele votou no painel eletrônico para o projeto de lei correspondente.

## 2. O que ESTÁ no escopo (In-Scope)
* **Público-Alvo Analisado:** Deputados Federais e Senadores da legislatura atual (a partir de 2023).
* **Fontes de Dados:** Projetos de Lei (PLs), Propostas de Emenda à Constituição (PECs), Discursos no Plenário e Votações Nominais extraídos via API Oficial.
* **Inteligência Artificial:** Uso de Busca Vetorial Semântica (RAG via Supabase/pgvector) e processamento de linguagem natural (Llama 3) para identificar a postura do discurso (A favor, Contra, Neutro).
* **Interface do Usuário (MVP):** Aplicação Web acessível (sem necessidade de login), contendo barra de busca de políticos, perfil individual, ranking geral e o comparador de coerência.

## 3. O que NÃO ESTÁ no escopo (Out-of-Scope)
* **Análise de Redes Sociais:** O sistema **não** avalia postagens do Twitter (X), Instagram, Facebook ou entrevistas na TV. Apenas discursos proferidos sob registro taquigráfico oficial.
* **Esfera Estadual e Municipal:** Deputados Estaduais, Vereadores, Prefeitos e Governadores não serão incluídos nesta versão.
* **Poder Executivo e Judiciário:** Avaliação de Ministros, Juízes ou do Presidente da República.
* **Análise de Projetos Menores:** Moções de aplauso, homenagens e requerimentos procedimentais serão filtrados e ignorados pelo motor de IA devido à baixa relevância semântica.
