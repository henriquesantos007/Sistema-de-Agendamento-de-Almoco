# desempenho Specification

## Purpose
Garantir tempos de resposta aceitáveis para o volume esperado de usuários do Centro de Informática.

## Requirements

### Requirement: NF-DES-01 — Tempo de cadastro
O sistema DEVE concluir o cadastro de 1 usuário em no máximo 1 segundo quando já houver 10.000 usuários cadastrados, em qualquer mecanismo de armazenamento.

**Prioridade:** Importante
**Casos de uso:** UC05

#### Scenario: Cadastro com 10.000 usuários existentes
- **GIVEN** existem 10.000 usuários cadastrados no armazenamento escolhido (memória ou arquivo)
- **WHEN** o Administrador cadastra mais 1 usuário válido
- **THEN** a operação termina em até 1 s, medido com `time.perf_counter`

### Requirement: NF-DES-02 — Tempo de listagem e de carga
O sistema DEVE listar 10.000 usuários em no máximo 100 ms e carregar um arquivo com 10.000 usuários em no máximo 1 segundo.

**Prioridade:** Importante
**Casos de uso:** UC06

#### Scenario: Listagem de 10.000 usuários
- **GIVEN** existem 10.000 usuários cadastrados
- **WHEN** o Administrador solicita a listagem
- **THEN** a lista com os 10.000 usuários é obtida em até 100 ms, medido com `time.perf_counter`

#### Scenario: Carga do arquivo com 10.000 usuários
- **GIVEN** o arquivo "dados/usuarios.bin" contém 10.000 usuários
- **WHEN** o sistema é iniciado com `--armazenamento arquivo`
- **THEN** o arquivo é carregado em até 1 s, medido com `time.perf_counter`
