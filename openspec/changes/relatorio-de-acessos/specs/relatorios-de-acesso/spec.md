## ADDED Requirements

### Requirement: RF16 — Consultar estatísticas de acesso
O sistema DEVE permitir que o Administrador consulte, a partir dos registros de acesso disponíveis, a quantidade total de acessos, a quantidade de usuários distintos com acesso e a quantidade de acessos por usuário. O detalhamento DEVE identificar cada usuário por id, login e perfil, sem expor senha ou e-mail.

**Prioridade:** Essencial
**Casos de uso:** UC22

#### Scenario: Relatório com acessos
- **GIVEN** há 5 registros de acesso disponíveis, distribuídos entre 2 usuários, sendo 3 do usuário "ana" e 2 do usuário "bruno"
- **WHEN** o Administrador consulta as estatísticas de acesso
- **THEN** o sistema apresenta total de 5 acessos, 2 usuários distintos e os respectivos totais por usuário
- **AND** o detalhamento identifica cada usuário por id, login e perfil
- **AND** o relatório não apresenta senha nem e-mail

#### Scenario: Nenhum acesso disponível
- **GIVEN** não há registros de acesso disponíveis
- **WHEN** o Administrador consulta as estatísticas de acesso
- **THEN** o sistema apresenta total de 0 acessos e 0 usuários distintos, sem linhas de detalhamento

### Requirement: RF17 — Gerar relatório de acessos em HTML ou CSV
O sistema DEVE disponibilizar as estatísticas de acesso nos formatos HTML e CSV. Ambos os formatos DEVEM apresentar o mesmo total de acessos, quantidade de usuários distintos e detalhamento por usuário definidos em RF16.

**Prioridade:** Importante
**Casos de uso:** UC22

#### Scenario: Geração em HTML
- **GIVEN** há registros de acesso disponíveis
- **WHEN** o Administrador solicita o relatório no formato HTML
- **THEN** o sistema disponibiliza um documento HTML com o resumo e o detalhamento definidos em RF16

#### Scenario: Geração em CSV
- **GIVEN** há registros de acesso disponíveis
- **WHEN** o Administrador solicita o relatório no formato CSV
- **THEN** o sistema disponibiliza um documento CSV com os mesmos dados do relatório HTML

#### Scenario: Formato não suportado
- **GIVEN** o Administrador solicita um formato diferente de HTML ou CSV
- **WHEN** o sistema valida a solicitação
- **THEN** o sistema recusa a geração e informa que os formatos aceitos são HTML e CSV
