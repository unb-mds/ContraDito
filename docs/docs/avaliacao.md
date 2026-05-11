# Avaliação Final e Relevância

O desenvolvimento do **ContraDito** representou um desafio complexo e gratificante no escopo da disciplina de Métodos de Desenvolvimento de Software (MDS) da Universidade de Brasília (UnB - FCTE). Esta seção consolida a avaliação final do produto entregue, destacando seu impacto cívico e as conquistas de engenharia alcançadas pela equipe.

## 1. Relevância Social e Produto

O ecossistema político brasileiro é denso e, muitas vezes, opaco para o eleitor comum. O ContraDito cumpre com excelência o seu objetivo principal: **reduzir a assimetria de informação**. 

Ao traduzir o volume massivo de discursos e registros de votações em um único "Score de Coerência", a plataforma entrega uma métrica compreensível e direta. A capacidade da ferramenta de expor contradições — ou confirmar a integridade política — empodera a sociedade civil com inteligência de dados, promovendo um controle social mais eficiente e fundamentado em fatos.

## 2. Avaliação Técnica (O Triunfo Técnico)

Sob a ótica da engenharia de software, o projeto estabeleceu um padrão de excelência ao adotar uma arquitetura moderna, escalável e resiliente. Os principais destaques técnicos incluem:

* **Arquitetura Orientada a Microsserviços:** A orquestração via Docker Compose garantiu um ambiente de desenvolvimento e deploy padronizado, isolando responsabilidades de forma eficaz.
* **Isolamento do Motor NLP:** A decisão de manter o Worker NLP (PyTorch/SBERT) enclausurado na rede interna demonstrou maturidade em segurança e gestão de recursos. Ele opera exclusivamente focado na geração de embeddings, sem exposição desnecessária.
* **Performance e Escalabilidade:** A adoção de Layer Caching otimizado e do FastAPI como roteador principal garantiu respostas ágeis. A preparação estrutural do banco vetorial (`pgvector` local escalando para Supabase) mostra visão de futuro para o ambiente de produção.
* **Agnosticismo de Hardware:** A infraestrutura multi-arquitetura (rodando nativamente em Apple Silicon/ARM64 e AMD64) eliminou gargalos no ambiente de desenvolvimento da equipe.

## 3. Maturidade na Regra de Negócio

A construção de um sistema de pontuação política exige extrema cautela. O grande êxito do ContraDito foi ir além do cruzamento binário de palavras. 

A implementação de mitigações na fórmula do Score de Coerência provou a sofisticação da análise. Ao instruir a IA a considerar o fator temporal e o contexto político intrincado — como os votos em "Destaques" —, o sistema evita a penalização injusta dos parlamentares devido a meras manobras regimentais. Isso garante uma blindagem lógica e aumenta a confiabilidade da métrica gerada.

## 4. Conclusão

O ContraDito transcende o status de um projeto acadêmico tradicional. A equipe aplicou rigor metodológico, práticas avançadas de DevOps, inteligência artificial e design de interfaces focado no usuário (Next.js) para construir uma solução real para um problema real. O resultado é um produto íntegro, tecnicamente sofisticado e de alto valor público.