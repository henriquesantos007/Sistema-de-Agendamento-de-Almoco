## MODIFIED Requirements

### Requirement: NF-SEG-01 — Não exibir senhas
O sistema NÃO DEVE exibir a senha (nem o seu hash) na listagem de usuários nem nas mensagens de validação.

**Prioridade:** Essencial
**Casos de uso:** UC06, UC08, UC10

#### Scenario: Listagem sem senhas
- **GIVEN** existem 3 usuários cadastrados
- **WHEN** o Administrador solicita a listagem
- **THEN** a saída contém 0 ocorrências das senhas cadastradas e 0 ocorrências do texto "pbkdf2_sha256"

#### Scenario: Mensagem de validação sem a senha
- **WHEN** o Administrador tenta cadastrar a senha "curta"
- **THEN** as mensagens de recusa contêm 0 ocorrências do texto "curta"

#### Scenario: Mensagem de validação da atualização sem a senha
- **WHEN** o Administrador tenta atualizar um usuário com a senha "curta"
- **THEN** a mensagem de recusa contém 0 ocorrências do texto "curta"

### Requirement: NF-SEG-02 — Armazenar apenas o hash da senha
O sistema DEVE armazenar a senha somente como hash PBKDF2-SHA256 com sal aleatório de 16 bytes e 600.000 iterações, nunca em texto puro.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC08

#### Scenario: Arquivo de dados sem senha em texto puro
- **GIVEN** o armazenamento em arquivo está ativo
- **WHEN** o Administrador cadastra um usuário com a senha "Reserva#2026"
- **THEN** o arquivo "dados/usuarios.bin" contém 0 ocorrências do texto "Reserva#2026"

#### Scenario: Mesma senha gera hashes diferentes
- **WHEN** dois usuários são cadastrados com a mesma senha "Reserva#2026"
- **THEN** os 2 hashes armazenados são diferentes

#### Scenario: Senha alterada é armazenada como hash
- **GIVEN** o armazenamento em arquivo está ativo e o usuário de id 1 possui uma senha armazenada como hash
- **WHEN** o Administrador atualiza a senha do usuário 1 para "NovaReserva#2026"
- **THEN** a senha atualizada é armazenada como hash PBKDF2-SHA256 com sal aleatório de 16 bytes e 600.000 iterações
- **AND** o arquivo "dados/usuarios.bin" contém 0 ocorrências do texto "NovaReserva#2026"

#### Scenario: Atualizações da mesma senha geram hashes diferentes
- **WHEN** dois usuários têm suas senhas atualizadas para "NovaReserva#2026"
- **THEN** os 2 hashes armazenados são diferentes
