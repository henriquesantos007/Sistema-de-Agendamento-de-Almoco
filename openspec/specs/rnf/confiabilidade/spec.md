# confiabilidade Specification

## Purpose
Garantir que falhas de leitura ou gravação no armazenamento não corrompam os dados nem encerrem o sistema de forma inesperada.

## Requirements

### Requirement: NF-CON-01 — Preservar os dados em falha de gravação
O sistema DEVE, quando não conseguir gravar um usuário ou um restaurante no arquivo binário, reportar a falha ao usuário, manter o arquivo existente intacto e descartar a operação que falhou.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC12

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

### Requirement: NF-CON-02 — Recusar arquivo de dados corrompido
O sistema DEVE recusar iniciar com um arquivo de dados corrompido, informando o motivo, em vez de carregar dados inválidos ou encerrar com erro não tratado.

**Prioridade:** Importante
**Casos de uso:** UC05, UC06, UC12, UC14

#### Scenario: Arquivo com conteúdo inválido
- **GIVEN** o arquivo "dados/usuarios.bin" ou o arquivo "dados/restaurantes.bin" contém bytes que não foram gerados pelo sistema
- **WHEN** o sistema é iniciado com `--armazenamento arquivo`
- **THEN** o sistema exibe 1 mensagem iniciada por "Não foi possível iniciar o armazenamento" e encerra
- **AND** 0 rastros de pilha (traceback) do Python são exibidos
