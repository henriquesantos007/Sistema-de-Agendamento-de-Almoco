# ADR-0002: Organizar a estrutura inicial por camadas

- Status: Aceito
- Data: 2026-09-30
- Origem: merge `153913a` (`chore(arquitetura): criar estrutura inicial de pacotes`), proveniente da branch `chore/pac-pacotes-iniciais`

## Contexto

Após a definição dos casos de uso e das classes de análise no PR #1, o repositório precisava de uma estrutura inicial para receber a implementação. O merge criou diretórios separados para apresentação web, aplicação, domínio e persistência em memória.

## Decisão

Organizar o código inicialmente por camadas, usando `source/apresentacao/web`, `source/aplicacao/usuarios`, `source/dominio/usuarios` e `source/infraestrutura/persistencia/memoria`. Novas áreas podem ser adicionadas conforme os módulos forem implementados.

## Consequências

- As responsabilidades definidas nos diagramas têm locais distintos na estrutura do código.
- A persistência em memória fica isolada da lógica de aplicação e do domínio.
- Os diretórios criados são apenas a estrutura inicial; sua existência não implica que todas as funcionalidades já estejam implementadas.

## Alternativas consideradas

- Colocar todas as classes em um único diretório; rejeitada por misturar responsabilidades.
