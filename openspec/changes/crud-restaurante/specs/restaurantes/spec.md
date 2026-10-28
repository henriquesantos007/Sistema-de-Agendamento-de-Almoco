## ADDED Requirements

### Requirement: RF07 — Cadastrar restaurante
O sistema DEVE cadastrar um restaurante quando receber nome, localização, telefone e horário limite de agendamento, com descrição opcional, gerando automaticamente o identificador e a data de cadastro e iniciando o restaurante com status ATIVO. Espaços no início e no fim dos textos são removidos.

**Prioridade:** Essencial
**Casos de uso:** UC12, UC18

#### Scenario: Cadastro válido gera identificador
- **GIVEN** não há restaurantes cadastrados
- **WHEN** o Administrador cadastra o restaurante com nome "Restaurante do CI", localização "Centro de Informática", telefone "83977770000", horário limite 10:30 e sem descrição
- **THEN** o restaurante recebe o id 1, gerado pelo sistema, com status ATIVO e descrição vazia
- **AND** a listagem de restaurantes passa a conter exatamente 1 linha: "[1] Restaurante do CI | Centro de Informática"

#### Scenario: Espaços nas pontas são removidos
- **WHEN** o Administrador cadastra o restaurante com nome "  Restaurante do CI "
- **THEN** o restaurante é cadastrado com o nome "Restaurante do CI"

#### Scenario: Campos obrigatórios ausentes
- **WHEN** o Administrador tenta cadastrar um restaurante com nome, localização e telefone vazios e sem horário limite
- **THEN** o sistema recusa o cadastro informando, de uma só vez, os 4 motivos: "nome e obrigatorio", "localizacao e obrigatorio", "telefone e obrigatorio" e "horario limite de agendamento invalido"
- **AND** a quantidade de restaurantes cadastrados continua 0

### Requirement: RF08 — Consultar restaurante pelo identificador
O sistema DEVE devolver os dados de um restaurante a partir do seu identificador.

**Prioridade:** Importante
**Casos de uso:** UC13

#### Scenario: Restaurante existente
- **GIVEN** o restaurante "Restaurante do CI" está cadastrado com o id 1
- **WHEN** o Administrador consulta o restaurante de id 1
- **THEN** o sistema devolve nome "Restaurante do CI", localização, telefone, horário limite, status e data de cadastro

#### Scenario: Restaurante inexistente
- **GIVEN** não existe restaurante com o id 99
- **WHEN** o Administrador consulta o restaurante de id 99
- **THEN** o sistema informa "restaurante nao encontrado: 99"

### Requirement: RF09 — Listar restaurantes
O sistema DEVE listar todos os restaurantes cadastrados, exibindo para cada um o id, o nome e a localização, na ordem de cadastro.

**Prioridade:** Essencial
**Casos de uso:** UC14

#### Scenario: Listagem com restaurantes
- **GIVEN** foram cadastrados, nesta ordem, "Restaurante do CI" (Centro de Informática) e "Sabor da Terra" (CCEN)
- **WHEN** o Administrador solicita a listagem de restaurantes
- **THEN** o sistema exibe exatamente 2 linhas, nesta ordem: "[1] Restaurante do CI | Centro de Informática" e "[2] Sabor da Terra | CCEN"

#### Scenario: Listagem vazia
- **GIVEN** não há restaurantes cadastrados
- **WHEN** o Administrador solicita a listagem de restaurantes
- **THEN** o sistema exibe 0 restaurantes

### Requirement: RF10 — Atualizar restaurante
O sistema DEVE permitir alterar nome, descrição, localização, telefone e horário limite de um restaurante cadastrado, aplicando as mesmas regras do cadastro e sem alterar o identificador nem a data de cadastro.

**Prioridade:** Essencial
**Casos de uso:** UC15, UC18

#### Scenario: Atualização válida
- **GIVEN** o restaurante de id 1 se chama "Restaurante do CI" e tem horário limite 10:30
- **WHEN** o Administrador atualiza o restaurante 1 para nome "RU do CI" e horário limite 11:00
- **THEN** a consulta do restaurante 1 devolve nome "RU do CI" e horário limite 11:00
- **AND** o id continua 1 e a data de cadastro continua a mesma

#### Scenario: Atualização com dados inválidos
- **GIVEN** o restaurante de id 1 se chama "RU do CI"
- **WHEN** o Administrador tenta atualizar o restaurante 1 com o nome vazio
- **THEN** o sistema recusa a atualização informando "nome e obrigatorio"
- **AND** o restaurante 1 continua com o nome "RU do CI"

#### Scenario: Restaurante inexistente
- **GIVEN** não existe restaurante com o id 99
- **WHEN** o Administrador tenta atualizar o restaurante 99
- **THEN** o sistema informa "restaurante nao encontrado: 99"

### Requirement: RF11 — Remover restaurante
O sistema DEVE remover um restaurante cadastrado, e NÃO DEVE remover um restaurante enquanto houver Gestor de Restaurante vinculado a ele.

**Prioridade:** Essencial
**Casos de uso:** UC16

#### Scenario: Remoção sem gestores vinculados
- **GIVEN** os restaurantes 1 e 2 estão cadastrados e nenhum gestor está vinculado ao restaurante 2
- **WHEN** o Administrador remove o restaurante 2
- **THEN** o sistema informa "Restaurante 2 removido."
- **AND** a listagem de restaurantes passa a conter apenas o restaurante 1

#### Scenario: Restaurante com gestor vinculado
- **GIVEN** o Gestor de Restaurante "carlossouza" está vinculado ao restaurante 1
- **WHEN** o Administrador tenta remover o restaurante 1
- **THEN** o sistema recusa a remoção informando "Remoção recusada: restaurante 1 possui gestores vinculados"
- **AND** o restaurante 1 continua na listagem

#### Scenario: Restaurante inexistente
- **GIVEN** não existe restaurante com o id 99
- **WHEN** o Administrador tenta remover o restaurante 99
- **THEN** o sistema informa "Remoção recusada: restaurante 99 não encontrado."
