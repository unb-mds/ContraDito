# Próximos Passos (Roadmap)

A arquitetura atual do **ContraDito** estabelece uma fundação escalável e resiliente. Com o processamento de linguagem natural (NLP) e o banco vetorial consolidados, o projeto possui um vasto horizonte de evolução técnica e de produto. Abaixo estão as iniciativas mapeadas para os próximos ciclos de desenvolvimento.

## 1. Retenção e Personalização de Usuários
* **Autenticação Não Obrigatória (Soft Login):** Implementação de um sistema de login opcional (OAuth2 via Google/GitHub), permitindo o acesso anônimo para consultas básicas, mas oferecendo vantagens para usuários cadastrados.
* **Monitoramento Personalizado:** Criação de um sistema de favoritos para que o eleitor possa criar uma carteira personalizada de parlamentares (ex: acompanhar apenas a bancada do seu estado).
* **Motor de Alertas:** Integração de um serviço de mensageria para envio de notificações por e-mail sobre novos discursos, pautas de votação iminentes ou variações significativas no Score de Coerência dos políticos favoritados.

## 2. Evolução Analítica e Histórica
* **Série Histórica do Score:** Transformação do Score de Coerência atual (que é um retrato de momento) em um gráfico de linha do tempo. Isso permitirá visualizar se o político perdeu ou ganhou coerência ao longo de todo o seu mandato.
* **Extração Temática (Topic Modeling):** Expansão do uso do nosso motor PyTorch/SBERT não apenas para similaridade, mas para clusterização de temas. O objetivo é gerar resumos visuais mostrando os tópicos mais falados pelo político em contraste com os temas em que ele mais vota.

## 3. Ecossistema e Acesso aos Dados
* **API Pública para Jornalistas e Pesquisadores:** Estruturação de rotas públicas no nosso backend FastAPI, protegidas por *rate limiting* e chaves de API. Isso transformará o ContraDito em um provedor de dados B2B para ONGs e veículos de mídia investigativa.
* **Transição para Near Real-Time:** Evolução do pipeline de ETL (atualmente em *batch*) para uma arquitetura orientada a eventos (*webhooks* ou *polling* de alta frequência) junto às APIs da Câmara e do Senado, reduzindo o tempo entre um discurso proferido e seu processamento na plataforma.