## ADDED Requirements

### Requirement: RF18 — Desfazer a última atualização de usuário
O sistema DEVE permitir ao Administrador desfazer a atualização de usuário concluída com sucesso mais recentemente durante a execução atual. Ao fazê-lo, o sistema DEVE restaurar e persistir o estado do usuário imediatamente anterior à atualização. O sistema DEVE manter disponível somente uma atualização para desfazer.

**Prioridade:** Essencial
**Casos de uso:** UC23

#### Scenario: Desfazer a atualização mais recente
- **GIVEN** o usuário de id 1 tinha o nome "Victor" e a atualização mais recente alterou o nome para "Victor Silva"
- **WHEN** o Administrador solicita o desfazimento da última atualização
- **THEN** o sistema restaura e persiste o nome "Victor" para o usuário de id 1
- **AND** preserva o identificador, o perfil e os dados específicos do perfil
- **AND** não mantém uma atualização disponível para desfazer

#### Scenario: Desfazer quando não há atualização disponível
- **GIVEN** não há atualização concluída disponível para desfazer na execução atual
- **WHEN** o Administrador solicita o desfazimento
- **THEN** o sistema não altera nenhum usuário
- **AND** informa "Aviso: Não há atualização disponível para desfazer."

#### Scenario: Desfazer somente a atualização mais recente
- **GIVEN** o usuário de id 1 foi atualizado com sucesso duas vezes durante a execução atual
- **WHEN** o Administrador solicita o desfazimento
- **THEN** o sistema restaura e persiste o estado do usuário imediatamente anterior à segunda atualização
- **AND** uma nova solicitação de desfazimento não altera o usuário

#### Scenario: Atualização inválida não descarta o histórico válido
- **GIVEN** o usuário de id 1 teve uma atualização concluída com sucesso e uma atualização posterior é recusada por dados inválidos
- **WHEN** o Administrador solicita o desfazimento
- **THEN** o sistema restaura e persiste o estado anterior à última atualização válida
- **AND** mantém disponível somente essa ação até que ela seja utilizada

#### Scenario: Desfazimento persiste em armazenamento de arquivo
- **GIVEN** o sistema usa armazenamento em arquivo e há uma atualização disponível para desfazer
- **WHEN** o Administrador solicita o desfazimento e o sistema é iniciado novamente
- **THEN** o usuário mantém o estado anterior à atualização, lido do arquivo

#### Scenario: Remoção invalida o desfazimento da atualização do mesmo usuário
- **GIVEN** o usuário de id 1 teve uma atualização concluída com sucesso
- **WHEN** o Administrador remove o usuário de id 1
- **THEN** o sistema descarta a ação disponível para desfazer essa atualização
- **AND** uma solicitação de desfazimento não altera nenhum usuário

#### Scenario: Falha ao persistir o desfazimento
- **GIVEN** há uma atualização disponível para desfazer e a gravação do arquivo falha
- **WHEN** o Administrador solicita o desfazimento
- **THEN** o sistema informa a falha de persistência e mantém o estado atualizado
- **AND** mantém disponível o desfazimento para uma nova tentativa
