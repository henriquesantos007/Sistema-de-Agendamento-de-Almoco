# usuarios Specification

## Purpose
Gerenciamento dos usuários do sistema (Administrador, Estudante e Gestor de Restaurante): cadastro com validação rigorosa de login e senha, e listagem.

## Requirements

### Requirement: RF01 — Cadastrar usuário
O sistema DEVE permitir o cadastro de novos usuários informando login, senha e papel (Administrador, Estudante ou Gestor de Restaurante), recusando logins já existentes.

**Prioridade:** Essencial
**Casos de uso:** UC01

#### Scenario: Cadastro válido
- **GIVEN** não existe usuário com login "victor"
- **WHEN** o Administrador cadastra login "victor", senha "Reserva#2026" e papel Estudante
- **THEN** o usuário é armazenado com sucesso

#### Scenario: Login já existente
- **GIVEN** já existe um usuário com login "victor"
- **WHEN** o Administrador tenta cadastrar outro usuário com login "victor"
- **THEN** o sistema recusa o cadastro informando "Login já está em uso"

### Requirement: RF02 — Regras de login
O sistema DEVE aceitar apenas logins não vazios, com no máximo 12 caracteres e sem números.

**Prioridade:** Essencial
**Casos de uso:** UC01

#### Scenario: Login vazio
- **WHEN** o Administrador tenta cadastrar um usuário com login vazio
- **THEN** o sistema recusa o cadastro informando "Login não pode ser vazio"

#### Scenario: Login longo
- **WHEN** o Administrador informa o login "victorcommaisde12" (17 caracteres)
- **THEN** o sistema recusa o cadastro informando "Login deve ter no máximo 12 caracteres"

#### Scenario: Login com números
- **WHEN** o Administrador informa o login "victor2026"
- **THEN** o sistema recusa o cadastro informando "Login não pode conter números"

### Requirement: RF03 — Regras de senha
O sistema DEVE aceitar apenas senhas que sigam a política do AWS IAM: de 8 a 128 caracteres, com pelo menos 3 dos 4 tipos (maiúscula, minúscula, número, símbolo) e diferentes do login.

**Prioridade:** Essencial
**Casos de uso:** UC01

#### Scenario: Senha curta
- **WHEN** o Administrador informa a senha "Ab#1" (4 caracteres)
- **THEN** o sistema recusa o cadastro informando "Senha deve ter entre 8 e 128 caracteres"

#### Scenario: Senha com poucos tipos
- **WHEN** o Administrador informa a senha "senhaforte" (apenas minúsculas)
- **THEN** o sistema recusa o cadastro informando "Senha deve combinar pelo menos 3 tipos"

#### Scenario: Senha válida
- **WHEN** o Administrador informa a senha "Almoco#2026" (maiúscula, minúscula, símbolo e número)
- **THEN** a senha é aceita

#### Scenario: Senha igual ao login
- **WHEN** o Administrador informa login "victor" e senha "victor"
- **THEN** o sistema recusa o cadastro informando que a senha não pode ser igual ao login

### Requirement: RF04 — Listar usuários
O sistema DEVE permitir a listagem de todos os usuários cadastrados, exibindo o login e o papel, sem exibir a senha.

**Prioridade:** Essencial
**Casos de uso:** UC02

#### Scenario: Listagem de usuários
- **GIVEN** existem 3 usuários cadastrados
- **WHEN** o Administrador solicita a listagem
- **THEN** o sistema exibe os 3 usuários com seus respectivos papéis, omitindo as senhas