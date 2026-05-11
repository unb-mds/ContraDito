# Manual do Usuário

Bem-vindo ao manual de uso do **ContraDito**! Nossa plataforma foi projetada para ser uma ferramenta de inteligência de dados com navegação intuitiva, focada na redução da assimetria de informação. Abaixo, detalhamos o fluxo da interface para que você possa extrair o máximo das nossas análises de coerência política.

## 1. Painel de Visão Geral (Hero Section)

Logo ao acessar o ContraDito, você encontrará a nossa *Hero Section*, que exibe as **Estatísticas Globais ao Vivo** do Congresso Nacional. Este painel consolida o pulso do cenário político brasileiro em tempo real, apresentando:

*   **Raio-X do Congresso:** O total de parlamentares monitorados ativamente (513 deputados federais e 81 senadores).
*   **Volume de Dados:** A quantidade de discursos proferidos em plenário que já foram processados e cruzados pelo nosso motor NLP.
*   **Média Nacional de Coerência:** Um termômetro geral, atualizado em tempo real, que indica o nível médio de alinhamento entre o que se fala e o que se vota no Brasil.

## 2. O Diretório de Políticos

A ferramenta central de pesquisa da plataforma é o **Diretório de Políticos**. É nesta seção que você pode investigar parlamentares específicos ou visualizar recortes geográficos e partidários.

### Busca Rápida
Se você já sabe quem deseja investigar, utilize a **Barra de Pesquisa**. Basta digitar o nome do parlamentar e o sistema filtrará os resultados instantaneamente.

### Filtros de Segmentação
Para análises mais amplas ou para monitorar bancadas específicas, utilize os filtros de seleção localizados junto à busca:
*   **Todos os Partidos:** Permite isolar os representantes de uma legenda partidária específica.
*   **Todos os Estados:** Permite filtrar pela Unidade Federativa (UF), ajudando você a acompanhar exclusivamente os políticos eleitos pelo seu estado.

## 3. Analisando os Resultados

Após realizar uma busca ou aplicar os filtros, a interface exibirá os dados cruzados em uma tabela de resultados objetiva. Cada linha da tabela é dedicada a um parlamentar e apresenta as seguintes informações:

*   **Nome:** Identificação do político.
*   **Partido:** Sigla da legenda atual.
*   **UF:** Estado de representação.
*   **Cargo:** Casa legislativa (Deputado Federal ou Senador).
*   **Score de Coerência (%):** O indicador principal da nossa inteligência. É uma nota de 0 a 100 que resume o grau de alinhamento matemático entre as falas do político e suas ações (votos) no plenário.

> **Quer aprofundar a análise?** 
> Para entender exatamente qual é a fórmula matemática por trás dessa nota e como a nossa inteligência artificial trata nuances e manobras regimentais, consulte a próxima página: [Entendendo o Score de Coerência](./calculo-score.md).