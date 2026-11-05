# confiabilidade Specification

## Purpose
Garantir que falhas de leitura ou gravação no armazenamento não corrompam os dados nem encerrem o sistema de forma inesperada.

## Requirements

### Requirement: NF-CON-01 — Preservar os dados em falha de gravação
O sistema DEVE, quando não conseguir gravar um usuário ou um restaurante no arquivo binário, reportar a falha ao usuário, manter o arquivo existente intacto e descartar a operação que falhou, preservando também o estado em memória anterior à operação.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC08, UC12, UC15, UC16, UC21

#### Scenario: Pasta de dados sem permissão de escrita
- **GIVEN** o armazenamento em arquivo contém 3 usuários
- **AND** a pasta "dados/" não permite gravação
- **WHEN** o Administrador cadastra um quarto usuário
- **THEN** o sistema exibe 1 mensagem iniciada por "Falha de persistência ao cadastrar" e continua em execução
- **AND** o arquivo "dados/usuarios.bin" tem 0 bytes alterados (mesmo hash SHA-256 de antes da operação)
- **AND** a listagem continua com 3 usuários

#### Scenario: Falha ao gravar restaurante
- **GIVEN** o armazenamento em arquivo contém 1 restaurante
- **AND** a pasta "dados/" não permite gravação
- **WHEN** o Administrador cadastra um segundo restaurante
- **THEN** o sistema exibe 1 mensagem iniciada por "Falha de persistência ao cadastrar" e continua em execução
- **AND** o arquivo "dados/restaurantes.bin" tem 0 bytes alterados e a quantidade de restaurantes continua 1

#### Scenario: Falha ao gravar atualização de usuário
- **GIVEN** o armazenamento em arquivo contém o usuário de id 1 com nome "Victor"
- **AND** a gravação do arquivo falha durante a atualização
- **WHEN** o Administrador atualiza o nome do usuário 1 para "Victor Silva"
- **THEN** o sistema exibe 1 mensagem iniciada por "Falha de persistência ao atualizar usuário 1" e continua em execução
- **AND** o arquivo "dados/usuarios.bin" mantém o mesmo hash SHA-256 de antes da operação
- **AND** o usuário de id 1 continua com o nome "Victor" na memória e após recarregar o arquivo

#### Scenario: Falha ao gravar remoção de usuário
- **GIVEN** o armazenamento em arquivo contém 2 usuários, incluindo o usuário de id 2
- **AND** a gravação do arquivo falha durante a remoção
- **WHEN** o Administrador remove o usuário 2
- **THEN** o sistema exibe 1 mensagem iniciada por "Falha de persistência ao remover o usuário 2" e continua em execução
- **AND** o arquivo "dados/usuarios.bin" mantém o mesmo hash SHA-256 de antes da operação
- **AND** os 2 usuários continuam presentes na memória e após recarregar o arquivo

#### Scenario: Falha ao gravar atualização de restaurante
- **GIVEN** o armazenamento em arquivo contém o restaurante de id 1 com nome "Restaurante do CI"
- **AND** a gravação do arquivo falha durante a atualização
- **WHEN** o Administrador atualiza o nome do restaurante 1 para "RU do CI"
- **THEN** o arquivo "dados/restaurantes.bin" mantém o mesmo hash SHA-256 de antes da operação
- **AND** o restaurante de id 1 continua com o nome "Restaurante do CI" na memória e após recarregar o arquivo

#### Scenario: Falha ao gravar remoção de restaurante
- **GIVEN** o armazenamento em arquivo contém 2 restaurantes, incluindo o restaurante de id 2
- **AND** a gravação do arquivo falha durante a remoção
- **WHEN** o Administrador remove o restaurante 2
- **THEN** o arquivo "dados/restaurantes.bin" mantém o mesmo hash SHA-256 de antes da operação
- **AND** os 2 restaurantes continuam presentes na memória e após recarregar o arquivo

### Requirement: NF-CON-02 — Recusar arquivo de dados corrompido
O sistema DEVE recusar iniciar com um arquivo de dados corrompido, informando o motivo, em vez de carregar dados inválidos ou encerrar com erro não tratado.

**Prioridade:** Importante
**Casos de uso:** UC05, UC06, UC12, UC14

#### Scenario: Arquivo com conteúdo inválido
- **GIVEN** o arquivo "dados/usuarios.bin" ou o arquivo "dados/restaurantes.bin" contém bytes que não foram gerados pelo sistema
- **WHEN** o sistema é iniciado com `--armazenamento arquivo`
- **THEN** o sistema exibe 1 mensagem iniciada por "Não foi possível iniciar o armazenamento" e encerra
- **AND** 0 rastros de pilha (traceback) do Python são exibidos
