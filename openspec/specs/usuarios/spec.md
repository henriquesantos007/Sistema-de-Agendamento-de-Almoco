# usuarios Specification

## Purpose
Gerenciamento dos usuários do sistema (Administrador, Estudante e Gestor de Restaurante): cadastro com validação de login e senha, impedimento de dados duplicados, listagem e escolha do mecanismo de armazenamento.

As mensagens entre aspas são exatamente as exibidas pelo sistema. Quando um cadastro é recusado por mais de um motivo, todas as mensagens são exibidas juntas (ver NF-USA-01).

## Requirements

### Requirement: RF01 — Cadastrar usuário
O sistema DEVE cadastrar um usuário quando receber perfil, nome, login, e-mail, senha e telefone válidos, além da matrícula (perfil Estudante) ou do restaurante (perfil Gestor de Restaurante), gerando automaticamente o identificador do usuário.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC01, UC11

#### Scenario: Cadastro válido gera identificador
- **GIVEN** não há usuários cadastrados
- **WHEN** o Administrador cadastra um Estudante com nome "Victor", login "victor", e-mail "victor@ci.ufpb.br", senha "Reserva#2026", telefone "83999990000" e matrícula "2026001"
- **THEN** o usuário recebe o id 1, gerado pelo sistema
- **AND** a listagem passa a conter exatamente 1 usuário: "[1] estudante | victor | victor@ci.ufpb.br"

#### Scenario: Campo obrigatório vazio
- **WHEN** o Administrador tenta cadastrar um usuário com o nome vazio
- **THEN** o sistema recusa o cadastro informando "nome e obrigatorio"

#### Scenario: E-mail em formato inválido
- **WHEN** o Administrador informa o e-mail "victor@"
- **THEN** o sistema recusa o cadastro informando "e-mail invalido"

#### Scenario: Perfil inexistente
- **WHEN** o Administrador informa o perfil "visitante"
- **THEN** o sistema recusa o cadastro informando "perfil invalido"

#### Scenario: Estudante sem matrícula
- **WHEN** o Administrador cadastra um Estudante sem informar a matrícula
- **THEN** o sistema recusa o cadastro informando "matricula e obrigatoria para estudante"

#### Scenario: Gestor sem restaurante
- **WHEN** o Administrador cadastra um Gestor de Restaurante sem informar o restaurante
- **THEN** o sistema recusa o cadastro informando "restaurante e obrigatorio para gestor"

#### Scenario: Gestor referencia restaurante inexistente
- **WHEN** o Administrador cadastra um Gestor de Restaurante com um identificador de restaurante que não está cadastrado
- **THEN** o sistema recusa o cadastro informando "restaurante nao encontrado"

### Requirement: RF02 — Regras de login
O sistema DEVE aceitar apenas logins não vazios, com no máximo 12 caracteres e sem números, desconsiderando espaços no início e no fim.

**Prioridade:** Essencial
**Casos de uso:** UC10

#### Scenario: Login vazio
- **WHEN** o Administrador informa o login "" (ou apenas espaços)
- **THEN** o sistema recusa o cadastro informando "login e obrigatorio"

#### Scenario: Login com exatamente 12 caracteres (limite)
- **WHEN** o Administrador informa o login "mariaeduarda" (12 caracteres)
- **THEN** o login é aceito

#### Scenario: Login com 13 caracteres (limite + 1)
- **WHEN** o Administrador informa o login "mariaeduardas" (13 caracteres)
- **THEN** o sistema recusa o cadastro informando "login deve ter no maximo 12 caracteres"

#### Scenario: Login com números
- **WHEN** o Administrador informa o login "victor2026"
- **THEN** o sistema recusa o cadastro informando "login nao pode conter numeros"

#### Scenario: Espaços nas pontas são removidos
- **WHEN** o Administrador informa o login " victor "
- **THEN** o usuário é cadastrado com o login "victor"

### Requirement: RF03 — Regras de senha
O sistema DEVE aceitar apenas senhas que sigam a política padrão do AWS IAM: de 8 a 128 caracteres, com pelo menos 3 dos 4 tipos de caracteres (maiúsculas, minúsculas, números e os especiais `! @ # $ % ^ & * ( ) _ + - = [ ] { } | '`) e diferentes do login e do e-mail.

**Prioridade:** Essencial
**Casos de uso:** UC10

#### Scenario: Senha com 8 caracteres (limite mínimo)
- **WHEN** o Administrador informa a senha "Almoco#1" (8 caracteres)
- **THEN** a senha é aceita

#### Scenario: Senha com 7 caracteres (limite mínimo − 1)
- **WHEN** o Administrador informa a senha "Almo#12" (7 caracteres)
- **THEN** o sistema recusa o cadastro informando "senha deve ter no minimo 8 caracteres"

#### Scenario: Senha com 128 caracteres (limite máximo)
- **WHEN** o Administrador informa uma senha de 128 caracteres: "Aa#1" seguido de 124 letras "a"
- **THEN** a senha é aceita

#### Scenario: Senha com 129 caracteres (limite máximo + 1)
- **WHEN** o Administrador informa uma senha de 129 caracteres: "Aa#1" seguido de 125 letras "a"
- **THEN** o sistema recusa o cadastro informando "senha deve ter no maximo 128 caracteres"

#### Scenario: Senha com exatamente 3 tipos de caracteres
- **WHEN** o Administrador informa a senha "almoco#2026" (minúsculas, especial e números)
- **THEN** a senha é aceita

#### Scenario: Senha com apenas 1 tipo de caractere
- **WHEN** o Administrador informa a senha "senhaforte" (apenas minúsculas)
- **THEN** o sistema recusa o cadastro informando "senha deve conter ao menos 3 dos 4 tipos de caracteres: maiusculas, minusculas, numeros e especiais (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ')"

#### Scenario: Senha igual ao login
- **WHEN** o Administrador informa o login "Almoco#CI" e a senha "Almoco#CI"
- **THEN** o sistema recusa o cadastro informando "senha nao pode ser identica ao login"

#### Scenario: Senha igual ao e-mail
- **WHEN** o Administrador informa o e-mail "ana.Silva@ci.br" e a senha "ana.Silva@ci.br"
- **THEN** o sistema recusa o cadastro informando "senha nao pode ser identica ao e-mail"

### Requirement: RF04 — Listar usuários
O sistema DEVE listar todos os usuários cadastrados, exibindo para cada um o id, o perfil, o login e o e-mail, na ordem de cadastro.

**Prioridade:** Essencial
**Casos de uso:** UC06

#### Scenario: Listagem com usuários
- **GIVEN** foram cadastrados, nesta ordem, os usuários "ana" (Estudante), "bia" (Gestor de Restaurante) e "caio" (Administrador)
- **WHEN** o Administrador solicita a listagem
- **THEN** o sistema exibe exatamente 3 linhas, nesta ordem: "[1] estudante | ana | ...", "[2] gestor_restaurante | bia | ..." e "[3] administrador | caio | ..."

#### Scenario: Listagem vazia
- **GIVEN** não há usuários cadastrados
- **WHEN** o Administrador solicita a listagem
- **THEN** o sistema exibe 0 usuários

### Requirement: RF05 — Escolher o mecanismo de armazenamento
O sistema DEVE permitir escolher, no início da execução, se os usuários e os restaurantes são armazenados em memória (padrão) ou em arquivo binário, com um arquivo para cada entidade.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC06, UC12, UC14

#### Scenario: Armazenamento padrão em memória
- **WHEN** o sistema é iniciado com `python main.py`, sem a opção `--armazenamento`
- **THEN** o sistema exibe "Armazenamento: memoria"
- **AND** ao encerrar, 0 usuários permanecem gravados

#### Scenario: Armazenamento em arquivo preserva os usuários
- **GIVEN** o sistema foi iniciado com `--armazenamento arquivo` e 1 usuário foi cadastrado
- **WHEN** o sistema é iniciado de novo com `--armazenamento arquivo`
- **THEN** a listagem exibe o mesmo usuário, com o mesmo id, lido de "dados/usuarios.bin"

#### Scenario: Armazenamento em arquivo preserva os restaurantes
- **GIVEN** o sistema foi iniciado com `--armazenamento arquivo` e 1 restaurante foi cadastrado
- **WHEN** o sistema é iniciado de novo com `--armazenamento arquivo`
- **THEN** a listagem de restaurantes exibe o mesmo restaurante, com o mesmo id, lido de "dados/restaurantes.bin"

#### Scenario: Caminhos dos arquivos informados na execução
- **WHEN** o sistema é iniciado com `--armazenamento arquivo --caminho dados/u.bin --caminho-restaurantes dados/r.bin`
- **THEN** os usuários são gravados em "dados/u.bin" e os restaurantes em "dados/r.bin"

#### Scenario: Mecanismo inexistente
- **WHEN** o sistema é iniciado com `--armazenamento xml`
- **THEN** o sistema não inicia e informa "invalid choice: 'xml' (choose from 'memoria', 'arquivo')"

### Requirement: RF06 — Impedir dados duplicados
O sistema NÃO DEVE cadastrar um usuário cujo login ou e-mail já pertença a outro usuário, nem um Estudante cuja matrícula ou telefone já pertença a outro Estudante. A comparação desconsidera maiúsculas/minúsculas e espaços nas pontas.

**Prioridade:** Essencial
**Casos de uso:** UC10

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
