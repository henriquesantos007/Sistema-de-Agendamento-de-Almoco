## ADDED Requirements

### Requirement: RF12 — Exibir resumo de entidades cadastradas
O sistema DEVE informar a quantidade de usuários cadastrados, a quantidade de restaurantes cadastrados e o total de entidades, igual à soma das duas quantidades.

**Prioridade:** Importante
**Casos de uso:** UC17

#### Scenario: Resumo com usuários e restaurantes
- **GIVEN** existem 2 usuários e 1 restaurante cadastrados
- **WHEN** o Administrador solicita o resumo de entidades
- **THEN** o sistema exibe "Usuários cadastrados: 2", "Restaurantes cadastrados: 1" e "Total de entidades cadastradas: 3"

#### Scenario: Resumo sem cadastros
- **GIVEN** não há usuários nem restaurantes cadastrados
- **WHEN** o Administrador solicita o resumo de entidades
- **THEN** o sistema exibe 0 usuários, 0 restaurantes e total 0

#### Scenario: Remoção atualiza o resumo
- **GIVEN** existem 1 usuário e 2 restaurantes cadastrados, e o resumo informa total 3
- **WHEN** o Administrador remove 1 restaurante sem gestores vinculados
- **THEN** o resumo passa a informar "Restaurantes cadastrados: 1" e "Total de entidades cadastradas: 2"
