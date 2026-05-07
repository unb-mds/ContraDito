# Frontend e Interface (Next.js & Tailwind CSS)

A interface do **ContraDito** foi projetada com foco na experiência do usuário (UX), especificamente voltada para a nossa persona principal: o jornalista investigativo. O objetivo é fornecer um painel rápido, responsivo, elegante e de fácil leitura para cruzamento de dados.

##  Arquitetura Base

O frontend foi construído utilizando **Next.js** com **React** e estilizado via **Tailwind CSS**. A estrutura de pastas segue o padrão moderno *App Router*:

* **Tela Inicial (O Diretório):** O arquivo `app/page.tsx` abriga a capa principal (Hero Section), a barra de busca com filtros cruzados (Partido/UF) e o ranking de políticos.
  * **Integração API:** Consome a rota `GET /api/politicos`.
* **Dossiê do Político (Rota Dinâmica):** O arquivo `app/politico/[id]/page.tsx` abriga a tela detalhada em formato *split* ou vertical, listando o histórico de discursos e as evidências (contradições) daquele parlamentar específico.
  * **Integração API:** Consome a rota `GET /api/politicos/{id_parlamentar}`.

##  Guia de Estilos e Design System

Para manter a identidade visual do projeto padronizada e transmitir a credibilidade necessária de uma ferramenta *GovTech*, adotamos as seguintes regras baseadas nas classes do Tailwind CSS:

* **Cores Principais:** O fundo padrão do sistema é predominantemente escuro (`bg-slate-900`) para transmitir seriedade jornalística e um tom de investigação profunda.
* **Tipografia:** Utilizamos fontes *clean* e modernas, representadas pelo padrão `font-sans` para garantir a leiturabilidade de textos longos.
* **Score de Coerência (Cores Semânticas):** O índice de contradição gerado pela IA utiliza cores com significado direto para facilitar a análise rápida pelo usuário:
  * **Notas altas (coerentes)** recebem obrigatoriamente a cor verde (`text-green-600`).
  * **Notas baixas (contraditórios)** recebem a cor vermelha (`text-red-600`).
* **Componentes Visuais:** Os *cards* de informação, tabelas e dossiês utilizam bordas suaves (`border-slate-300`) e fundos brancos (`bg-white`), criando um esquema de alto contraste perfeito para a leitura de dados governamentais.s