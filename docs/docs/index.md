# ContraDito

## Sobre

#  Bem-vindo ao ContraDito

**ContraDito** é uma plataforma de inteligência de dados e fiscalização social focada no cenário político brasileiro. Desenvolvido como projeto da disciplina de Métodos de Desenvolvimento de Software (MDS), o sistema utiliza Inteligência Artificial para cruzar o que os parlamentares falam com o que eles efetivamente votam.

---

##  Contextualização

No Brasil, a transparência pública avançou significativamente com a Lei de Acesso à Informação (LAI) e os portais de Dados Abertos do Governo Federal. Hoje, qualquer cidadão tem acesso a milhares de transcrições de discursos, projetos de lei (PLs, PECs) e registros de votações nominais. 

No entanto, o volume desses dados é massivo. Compreender se um político mantém uma postura coerente ao longo do tempo exige que o eleitor leia dezenas de ementas jurídicas complexas e assista a horas de discursos em plenário. A informação existe, mas a sua **acessibilidade cognitiva** ainda é uma barreira para a maioria da população.

---

##  Motivação

O projeto nasce da necessidade de combater a desinformação e a polarização através de dados concretos. Frequentemente, observa-se no cenário político o fenômeno do discurso duplo: um parlamentar pode proferir discursos inflamados a favor de um tema (para gerar engajamento nas redes sociais), mas votar de forma oposta ou abster-se quando o projeto vai a plenário.

A nossa motivação é **reduzir a assimetria de informação** entre o representante e o eleitor, automatizando o cruzamento desses dados e expondo contradições (ou confirmando coerências) de forma visual, rápida e isenta de viés ideológico.

---

##  Objetivos do Projeto

O objetivo central do ContraDito é fornecer uma ferramenta de auditoria cidadã acessível. Para alcançar isso, definimos os seguintes objetivos específicos:

1. **Ingestão Automatizada (ETL):** Consumir, higienizar e estruturar dados oficiais das APIs da Câmara dos Deputados e do Senado Federal.
2. **Busca Semântica (RAG):** Utilizar modelos de linguagem (NLP) e bancos de dados vetoriais para correlacionar o tema de uma votação com discursos passados do parlamentar sobre o mesmo assunto.
3. **Score de Coerência:** Calcular matematicamente um índice de fidelidade entre o discurso proferido e a ação legislativa tomada no painel eletrônico.
4. **Interface Clara:** Apresentar essas "provas" lado a lado em uma interface web intuitiva, permitindo que o cidadão tire as suas próprias conclusões.

> **O ContraDito não emite opiniões políticas.** O nosso papel é puramente tecnológico: organizar o caos informacional e colocar a fala e o voto frente a frente num "ringue" de dados públicos.

## Equipe

<div align="center">
  <table style="border: none; background-color: transparent;">
    <tr style="border: none; background-color: transparent;">
      <td align="center" style="border: none; background-color: transparent;">
        <a href="https://github.com/henriquemendeselias">
          <img src="https://avatars.githubusercontent.com/henriquemendeselias" width="115px;" style="border-radius: 50%;" alt="Henrique Mendes"/><br>
          <sub><b>Henrique Mendes</b></sub>
        </a>
      </td>
      <td align="center" style="border: none; background-color: transparent;">
        <a href="https://github.com/jot4-ge">
          <img src="https://avatars.githubusercontent.com/jot4-ge" width="115px;" style="border-radius: 50%;" alt="João Guilherme Amancio"/><br>
          <sub><b>João Guilherme Amancio</b></sub>
        </a>
      </td>
      <td align="center" style="border: none; background-color: transparent;">
        <a href="https://github.com/luizhtmoreira">
          <img src="https://avatars.githubusercontent.com/luizhtmoreira" width="115px;" style="border-radius: 50%;" alt="Luiz"/><br>
          <sub><b>Luiz</b></sub>
        </a>
      </td>
    </tr>
    <tr style="border: none; background-color: transparent;">
      <td align="center" style="border: none; background-color: transparent;">
        <a href="https://github.com/lucasaraujoszz">
          <img src="https://avatars.githubusercontent.com/lucasaraujoszz" width="115px;" style="border-radius: 50%;" alt="Lucas"/><br>
          <sub><b>Lucas</b></sub>
        </a>
      </td>
      <td align="center" style="border: none; background-color: transparent;">
        <a href="https://github.com/matheus0346">
          <img src="https://avatars.githubusercontent.com/matheus0346" width="115px;" style="border-radius: 50%;" alt="Matheus"/><br>
          <sub><b>Matheus</b></sub>
        </a>
      </td>
      <td align="center" style="border: none; background-color: transparent;">
        <a href="https://github.com/G2SBiell">
          <img src="https://avatars.githubusercontent.com/G2SBiell" width="115px;" style="border-radius: 50%;" alt="Gabriel Portacio"/><br>
          <sub><b>Gabriel Portacio</b></sub>
        </a>
      </td>
    </tr>
  </table>
</div>
