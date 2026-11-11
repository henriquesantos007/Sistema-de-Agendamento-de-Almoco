## ADDED Requirements

### Requirement: RF16 — Consultar estatísticas de acesso
O sistema DEVE permitir que o Administrador consulte, a partir dos registros de acesso disponíveis, a quantidade total de acessos, a quantidade de usuários distintos com acesso e a quantidade de acessos por usuário. O detalhamento DEVE identificar cada usuário por id, login e perfil, sem expor senha ou e-mail. Os registros de um usuário removido DEVEM continuar contando no total de acessos e na quantidade de usuários distintos; nesse caso, o detalhamento DEVE apresentar o id e indicar login e perfil como "usuário removido". As linhas do detalhamento DEVEM estar ordenadas pela quantidade de acessos, da maior para a menor; em caso de empate, pelo id do usuário, do menor para o maior.

**Prioridade:** Essencial
**Casos de uso:** UC22

#### Scenario: Relatório com acessos
- **GIVEN** há 5 registros de acesso disponíveis, distribuídos entre 2 usuários, sendo 3 do usuário "ana" e 2 do usuário "bruno"
- **WHEN** o Administrador consulta as estatísticas de acesso
- **THEN** o sistema apresenta total de 5 acessos, 2 usuários distintos e os respectivos totais por usuário
- **AND** o detalhamento apresenta "ana", com 3 acessos, antes de "bruno", com 2 acessos
- **AND** o detalhamento identifica cada usuário por id, login e perfil
- **AND** o relatório não apresenta senha nem e-mail

#### Scenario: Empate na quantidade de acessos
- **GIVEN** há 4 registros de acesso disponíveis, sendo 2 do usuário "carla", de id 5, e 2 do usuário "bruno", de id 2
- **WHEN** o Administrador consulta as estatísticas de acesso
- **THEN** o sistema apresenta total de 4 acessos e 2 usuários distintos
- **AND** o detalhamento apresenta "bruno" (id 2) antes de "carla" (id 5), ambos com 2 acessos

#### Scenario: Acessos de usuário removido
- **GIVEN** há 4 registros de acesso disponíveis, sendo 3 do usuário "ana" e 1 do usuário de id 7, removido depois do acesso
- **WHEN** o Administrador consulta as estatísticas de acesso
- **THEN** o sistema apresenta total de 4 acessos e 2 usuários distintos
- **AND** o detalhamento apresenta primeiro "ana", com 3 acessos, identificada por id, login e perfil
- **AND** o detalhamento apresenta em seguida 1 acesso para o id 7, com login e perfil indicados como "usuário removido"

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
- **GIVEN** há registros de acesso disponíveis
- **WHEN** o Administrador solicita o relatório no formato PDF
- **THEN** o sistema recusa a geração, sem disponibilizar documento
- **AND** informa que os formatos aceitos são HTML e CSV
