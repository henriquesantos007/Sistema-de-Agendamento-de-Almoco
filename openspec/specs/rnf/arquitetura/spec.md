# arquitetura Specification

## Purpose
Garantir a flexibilidade da persistência e a robustez contra falhas de I/O.

## Requirements

### Requirement: NF-ARQ-01 — Persistência substituível
O sistema DEVE permitir a troca do mecanismo de persistência (RAM ou Arquivo Binário) no início da execução.

**Prioridade:** Essencial

#### Scenario: Seleção de persistência
- **GIVEN** o sistema possui repositórios de Memória e Arquivo
- **WHEN** o sistema é iniciado com a configuração de Arquivo Binário
- **THEN** 100% dos usuários são salvos no arquivo físico

### Requirement: NF-ARQ-02 — Tolerância a falha de armazenamento
O sistema DEVE tratar exceções de persistência (como `IOException` ou `SQLException`) sem quebrar a execução.

**Prioridade:** Essencial

#### Scenario: Falha ao salvar no arquivo
- **GIVEN** o arquivo binário está bloqueado pelo sistema operacional
- **WHEN** ocorre uma tentativa de salvar um usuário
- **THEN** 1 exceção é capturada e tratada internamente sem encerrar o programa