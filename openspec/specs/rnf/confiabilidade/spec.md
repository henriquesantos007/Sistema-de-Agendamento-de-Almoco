# confiabilidade Specification

## Purpose
Garantir que falhas de leitura ou gravação no armazenamento não corrompam os dados nem encerrem o sistema de forma inesperada.

## Requirements

### Requirement: NF-CON-01 — Preservar os dados em falha de gravação
O sistema DEVE, quando não conseguir gravar um usuário no arquivo binário, reportar a falha ao usuário, manter o arquivo existente intacto e descartar o cadastro que falhou.

**Prioridade:** Essencial
**Casos de uso:** UC05

#### Scenario: Pasta de dados sem permissão de escrita
- **GIVEN** o armazenamento em arquivo contém 3 usuários
- **AND** a pasta "dados/" não permite gravação
- **WHEN** o Administrador cadastra um quarto usuário
- **THEN** o sistema exibe 1 mensagem iniciada por "Falha de persistencia ao cadastrar" e continua em execução
- **AND** o arquivo "dados/usuarios.bin" tem 0 bytes alterados (mesmo hash SHA-256 de antes da operação)
- **AND** a listagem continua com 3 usuários

### Requirement: NF-CON-02 — Recusar arquivo de dados corrompido
O sistema DEVE recusar iniciar com um arquivo de dados corrompido, informando o motivo, em vez de carregar dados inválidos ou encerrar com erro não tratado.

**Prioridade:** Importante
**Casos de uso:** UC05, UC06

#### Scenario: Arquivo com conteúdo inválido
- **GIVEN** o arquivo "dados/usuarios.bin" contém bytes que não foram gerados pelo sistema
- **WHEN** o sistema é iniciado com `--armazenamento arquivo`
- **THEN** o sistema exibe 1 mensagem iniciada por "Nao foi possivel iniciar o armazenamento" e encerra
- **AND** 0 rastros de pilha (traceback) do Python são exibidos
