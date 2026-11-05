## MODIFIED Requirements

### Requirement: RF06 — Impedir dados duplicados
O sistema NÃO DEVE cadastrar nem atualizar um usuário de modo que seu login ou e-mail pertença a outro usuário, nem um Estudante de modo que sua matrícula ou telefone pertença a outro Estudante. Na atualização, os dados do próprio usuário não são considerados duplicados. A comparação desconsidera maiúsculas/minúsculas e espaços nas pontas.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC08, UC10

#### Scenario: Login já cadastrado
- **GIVEN** já existe um usuário com login "victor"
- **WHEN** o Administrador cadastra outro usuário com login " Victor "
- **THEN** o sistema recusa o cadastro informando "login ja cadastrado"
- **AND** a listagem continua com 1 usuário

#### Scenario: E-mail já cadastrado
- **GIVEN** já existe um usuário com e-mail "victor@ci.ufpb.br"
- **WHEN** o Administrador cadastra outro usuário com o mesmo e-mail
- **THEN** o sistema recusa o cadastro informando "e-mail ja cadastrado"

#### Scenario: Matrícula já cadastrada
- **GIVEN** já existe um Estudante com matrícula "2026001"
- **WHEN** o Administrador cadastra outro Estudante com a matrícula "2026001"
- **THEN** o sistema recusa o cadastro informando "matricula ja cadastrada"

#### Scenario: Atualização mantém os próprios dados únicos
- **GIVEN** o usuário de id 1 tem login "victor", e-mail "victor@ci.ufpb.br" e matrícula "2026001"
- **WHEN** o Administrador atualiza o usuário 1 mantendo esses dados
- **THEN** a atualização é aceita sem informar duplicidade

#### Scenario: Atualização usa dado único de outro usuário
- **GIVEN** o usuário de id 1 tem e-mail "victor@ci.ufpb.br" e o usuário de id 2 tem e-mail "ana@ci.ufpb.br"
- **WHEN** o Administrador tenta atualizar o usuário 1 para usar "ana@ci.ufpb.br"
- **THEN** o sistema recusa a atualização informando "e-mail ja cadastrado"

## ADDED Requirements

### Requirement: RF13 — Consultar usuário pelo identificador
O sistema DEVE devolver os dados de um usuário cadastrado a partir do seu identificador.

**Prioridade:** Importante
**Casos de uso:** UC20

#### Scenario: Usuário existente
- **GIVEN** o usuário "victor" está cadastrado com o id 1
- **WHEN** o Administrador consulta o usuário de id 1
- **THEN** o sistema devolve os dados do usuário de id 1

#### Scenario: Usuário inexistente
- **GIVEN** não existe usuário com o id 99
- **WHEN** o Administrador consulta o usuário de id 99
- **THEN** o sistema informa "Usuário com ID '99' não encontrado."

### Requirement: RF14 — Atualizar usuário
O sistema DEVE permitir atualizar nome, login, e-mail, senha e telefone de um usuário cadastrado, aplicando as regras de validação correspondentes e sem alterar seu identificador, perfil ou dados específicos do perfil.

**Prioridade:** Essencial
**Casos de uso:** UC08

#### Scenario: Atualização válida preserva o identificador e os dados do próprio usuário
- **GIVEN** o usuário Estudante de id 1 tem nome "Victor", login "victor", e-mail "victor@ci.ufpb.br", telefone "83999990000" e matrícula "2026001"
- **WHEN** o Administrador atualiza o usuário 1 para nome "Victor Silva" mantendo os demais dados válidos
- **THEN** o sistema atualiza o nome para "Victor Silva"
- **AND** o id continua 1, o perfil continua Estudante e a matrícula continua "2026001"

#### Scenario: Atualização com dados inválidos
- **GIVEN** o usuário de id 1 tem o e-mail "victor@ci.ufpb.br"
- **WHEN** o Administrador tenta atualizar o usuário 1 com um e-mail já pertencente ao usuário de id 2
- **THEN** o sistema recusa a atualização informando "Erros de validação: e-mail ja cadastrado"
- **AND** o usuário de id 1 permanece sem alterações

#### Scenario: Atualização de usuário inexistente
- **GIVEN** não existe usuário com o id 99
- **WHEN** o Administrador tenta atualizar o usuário 99
- **THEN** o sistema informa "Usuário com ID '99' não encontrado."

### Requirement: RF15 — Remover usuário
O sistema DEVE remover um usuário cadastrado a partir do seu identificador.

**Prioridade:** Essencial
**Casos de uso:** UC21

#### Scenario: Remoção de usuário existente
- **GIVEN** existem 2 usuários cadastrados e um deles tem o id 2
- **WHEN** o Administrador remove o usuário de id 2
- **THEN** o usuário de id 2 deixa de ser encontrado
- **AND** a quantidade de usuários cadastrados passa a ser 1

#### Scenario: Remoção de usuário inexistente
- **GIVEN** não existe usuário com o id 99
- **WHEN** o Administrador tenta remover o usuário 99
- **THEN** o sistema informa "Usuário com ID '99' não encontrado."
