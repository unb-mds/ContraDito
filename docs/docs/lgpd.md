# Transparência e LGPD

O **ContraDito** tem um compromisso inegociável com a transparência, a ética na análise de dados e a privacidade dos nossos usuários, em total conformidade com a **Lei Geral de Proteção de Dados (Lei nº 13.709/2018)**.

Este documento explica como tratamos as informações no nosso sistema, divididas em duas frentes: os dados públicos que analisamos e os dados dos usuários que acessam a plataforma.

---

## 1. Transparência na Análise de Dados Públicos (O Score de Coerência)

O principal objetivo do ContraDito é evidenciar a coerência entre o discurso e a prática de figuras públicas. Para isso, utilizamos Inteligência Artificial. É nosso dever explicar como chegamos a essas conclusões para evitar qualquer acusação de viés político:

* **Fonte dos Dados:** Não inventamos ou presumimos informações. Todos os discursos, projetos e votos analisados são extraídos exclusivamente das APIs de Dados Abertos da Câmara dos Deputados e do Senado Federal.
* **O Papel da Inteligência Artificial:** Abandonamos métodos subjetivos de análise de texto. Utilizamos uma arquitetura avançada chamada **RAG (Retrieval-Augmented Generation)**. A IA atua estritamente como uma ferramenta de leitura matemática, cruzando as ementas das leis com o que foi dito no plenário.
* **Cálculo do Score:** O *Score de Coerência* não é uma "opinião" do algoritmo. Ele é o resultado determinístico da **Similaridade de Cosseno** calculado no nosso banco de dados vetorial (Supabase). Ele mede a distância matemática entre o vetor do discurso proferido e a ação legislativa (voto) tomada.
* **Justificativas Auditáveis:** O sistema é desenhado para exibir as "Provas da Contradição" lado a lado, com links originais das fontes governamentais, permitindo que qualquer cidadão audite e tire as suas próprias conclusões.

---

## 2. Privacidade e Dados dos Usuários

Se você é um cidadão navegando no ContraDito, a sua privacidade é a nossa regra padrão.

### Quais dados coletamos e por quê?
* **Dados de Navegação:** Coletamos apenas métricas básicas e anônimas de acesso para entender o tráfego do site e garantir a estabilidade dos servidores.
* **Dados Pessoais e Cadastro:** Como esta ferramenta visa o acesso democrático e livre à informação, a nossa versão atual (MVP) **não exige criação de conta, login ou fornecimento de e-mail**. Portanto, não solicitamos, não armazenamos e não processamos dados sensíveis dos visitantes.

### Compartilhamento de Dados
**Nós não vendemos, alugamos ou repassamos nenhum dado para terceiros.** Como este é um projeto de código aberto nascido no ambiente acadêmico da Universidade de Brasília (UnB), o nosso compromisso é exclusivamente com o controle social e a fiscalização pública.
