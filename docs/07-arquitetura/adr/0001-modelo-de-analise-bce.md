# ADR-0001: Adotar o modelo de análise Fronteira-Controle-Entidade

- Status: Aceito
- Data: 2026-09-30
- Origem: PR #1, merge `8a639dd` (`docs(specs): adicionar documentos do Laboratório 1`)

## Contexto

Os casos de uso do sistema precisam ser representados de modo que interfaces, coordenação dos fluxos e dados do domínio tenham responsabilidades distintas. O PR #1 introduziu diagramas de análise com as classes de usuários e dos demais fluxos do sistema.

## Decisão

Adotar os estereótipos `Boundary`, `Control` e `Entity` nos modelos de análise e respeitar a comunicação Ator → Fronteira → Controle → Entidade. Fronteiras não acessam entidades diretamente, e entidades não dependem de fronteiras nem de controles.

## Consequências

- As telas e integrações externas ficam identificadas como fronteiras.
- Os controles coordenam casos de uso e validações.
- As entidades representam os dados e regras do domínio.
- Os diagramas e futuras implementações devem preservar essas responsabilidades e o sentido das dependências.

## Alternativas consideradas

- Permitir que telas consultem e alterem entidades diretamente; rejeitada por acoplar a interface aos dados e às regras do domínio.
- Não distinguir papéis no modelo; rejeitada por tornar menos claras as responsabilidades das classes de análise.