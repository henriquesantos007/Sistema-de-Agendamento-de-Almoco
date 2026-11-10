# ADR-0009: Aplicar Repository e Factory às entidades persistidas

- Status: Proposto
- Data: 2026-11-10

## Contexto

Os controladores e validadores precisam consultar e alterar dados sem depender
de como eles são armazenados. O projeto já define `RepositorioUsuarios` e
`RepositorioRestaurantes` como contratos no domínio, implementados em memória
e em arquivo na infraestrutura. A escolha da implementação ocorre no início
da execução pelas funções `criar_repositorio_usuarios` e
`criar_repositorio_restaurantes`, em
`source/infraestrutura/persistencia/fabrica_repositorio.py`.

A Sprint 4 solicita Repository para as entidades do projeto e Factory Method
ou Abstract Factory para criar entidades ou escolher o tipo de repositório. A
change `relatorio-de-acessos` prevê estatísticas calculadas a partir de
registros de acesso, mas a captura desses registros e o modelo definitivo
ainda precisam ser integrados à implementação.

## Decisão proposta

- Para cada entidade de domínio que tenha persistência própria, definir um
  contrato de repositório no domínio. A aplicação depende desses contratos, e
  não importa implementações concretas da infraestrutura.
- Implementar os contratos na infraestrutura, mantendo cada mecanismo de
  armazenamento substituível sem alterar as regras de negócio.
- Adotar Factory Method para escolher a implementação de repositório solicitada
  na composição da aplicação, estendendo as funções de fábrica existentes na
  infraestrutura. A seleção do armazenamento permanece fora do domínio e da
  aplicação.
- Aplicar o mesmo desenho ao registro de acesso que fornecerá os dados do
  relatório: contrato de repositório no domínio, implementação na
  infraestrutura e seleção pela fábrica. Os métodos do contrato devem cobrir
  as operações realmente necessárias ao registro e à consulta dos acessos.
- Manter a criação das entidades nas regras de domínio ou de aplicação; a
  fábrica seleciona repositórios, não substitui os construtores das entidades.
- Interpretar "todas as entidades" como todas as entidades que exijam
  armazenamento independente no escopo implementado. Objetos de valor e dados
  derivados de consultas não recebem repositórios próprios sem necessidade
  de persistência.

Os contratos e repositórios de usuários e restaurantes já atendem a esse
desenho. A extensão para registros de acesso é uma decisão planejada e não
declara que essa funcionalidade já esteja implementada.

## Consequências

- Controladores e validadores podem ser testados com implementações em memória
  ou substitutos dos contratos sem conhecer detalhes de arquivo.
- A infraestrutura permanece responsável por detalhes de armazenamento e
  pela seleção da implementação concreta.
- Uma nova entidade persistida exige contrato, implementação(ões), seleção
  pela fábrica e testes correspondentes.
- A entidade de acesso precisa ter um modelo e operações de consulta definidos
  antes de implementar seu repositório; esses detalhes não ficam fixados por
  esta ADR.
- A escolha atual entre memória e arquivo continua compatível com os
  repositórios já existentes; mecanismos adicionais dependem de decisão
  própria.

## Alternativas consideradas

- Fazer controladores acessarem diretamente as implementações de arquivo ou
  memória; rejeitada por acoplar as regras da aplicação aos detalhes de
  infraestrutura.
- Criar uma fábrica diferente em cada controlador; rejeitada por espalhar a
  seleção do armazenamento e dificultar a composição consistente.
- Criar repositórios para todo tipo de classe, incluindo objetos de valor e
  resultados calculados; rejeitada porque Repository se aplica a dados com
  ciclo de vida e persistência próprios, não a toda classe do modelo.
- Fazer a fábrica criar entidades de domínio; rejeitada porque a criação das
  entidades deve continuar sob responsabilidade das regras que conhecem suas
  invariantes, enquanto esta fábrica escolhe o mecanismo de persistência.

## Relação com decisões anteriores

Esta decisão consolida e estende o desenho já registrado em
[ADR-0003](./0003-persistencia-de-usuarios-em-binario.md) para usuários e em
[ADR-0006](./0006-persistencia-de-restaurantes-em-arquivo.md) para restaurantes.
Não substitui essas decisões nem altera os mecanismos existentes.
