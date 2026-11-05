# Casos de Uso Detalhados

Para a entrega, os três casos de uso selecionados como mais relevantes são
**UC05 — Cadastrar Usuário**, **UC12 — Cadastrar Restaurante** e
**UC16 — Remover Restaurante**. Eles cobrem o cadastro de usuários, o CRUD da
nova entidade e a regra de remoção condicionada ao vínculo com gestores.

Como documentação complementar, este arquivo também detalha
**UC08 — Editar Usuário**, **UC20 — Consultar Usuário** e
**UC21 — Remover Usuário**, operações implementadas no CRUD de usuários. Os atores,
precondições e fluxos seguem as
regras de [usuários](../../openspec/specs/usuarios/spec.md) e
[restaurantes](../../openspec/specs/restaurantes/spec.md), e os RNFs de
[segurança](../../openspec/specs/rnf/seguranca/spec.md),
[usabilidade](../../openspec/specs/rnf/usabilidade/spec.md) e
[confiabilidade](../../openspec/specs/rnf/confiabilidade/spec.md). As telas
descritas são conceituais; a interface executável atual continua sendo a CLI
de `main.py`.

## UC05 — Cadastrar Usuário

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Registrar uma conta de usuário com um perfil válido. |
| Precondições | O Administrador está autenticado. |
| Pós-condições | O usuário validado é persistido com identificador gerado; sua senha fica armazenada somente como hash. |

### Fluxo principal

1. O Administrador inicia o cadastro e escolhe Estudante, Gestor de Restaurante ou Administrador.
2. O sistema apresenta os campos comuns: nome, login, e-mail, senha e telefone.
3. O Administrador informa os dados e, conforme o perfil, a matrícula do Estudante ou o restaurante do Gestor.
4. O Administrador confirma o cadastro.
5. O sistema valida os campos, as regras de login e senha, os dados únicos e o vínculo do Gestor.
6. O sistema normaliza o perfil (remove espaços externos e converte para minúsculas), remove espaços externos do login, remove caracteres não numéricos do telefone, gera o hash da senha e cria o usuário com identificador. Nome, e-mail e matrícula são mantidos como informados.
7. O sistema persiste o usuário e confirma o cadastro, sem exibir a senha nem seu hash.

### Fluxos alternativos e de exceção

- **5a. Dados inválidos ou duplicados:** o sistema reúne e apresenta todos os motivos; nenhum usuário é cadastrado.
- **5b. Perfil Estudante sem matrícula:** o sistema informa que a matrícula é obrigatória e mantém o cadastro inalterado.
- **5c. Perfil Gestor sem restaurante ou com ID inexistente:** o sistema informa o motivo e não cria o usuário.
- **7a. Falha de persistência:** o sistema informa a falha e descarta a operação, preservando os dados anteriores.

## UC08 — Editar Usuário

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Atualizar os dados editáveis de um usuário cadastrado. |
| Precondições | O Administrador está autenticado e informa o identificador de um usuário existente. |
| Pós-condições | Nome, login, e-mail, senha e telefone são atualizados; o identificador, o perfil e os dados específicos do perfil são preservados. A senha permanece armazenada somente como hash. |

### Fluxo principal

1. O Administrador seleciona um usuário e solicita a edição.
2. O sistema localiza o usuário pelo identificador e apresenta os dados editáveis.
3. O Administrador informa nome, login, e-mail, senha e telefone, preservando os demais dados do usuário.
4. O Administrador confirma a atualização.
5. O sistema valida os campos e regras de login, senha e unicidade, ignorando os dados únicos que já pertencem ao usuário editado.
6. O sistema aplica as alterações sem modificar o identificador, o perfil, a matrícula ou o restaurante vinculado.
7. O sistema persiste a atualização e confirma o sucesso sem exibir a senha nem seu hash.

### Fluxos alternativos e de exceção

- **2a. Usuário inexistente:** o sistema informa "Usuário com ID '<id>' não encontrado." e não altera dados.
- **5a. Dados inválidos ou duplicados:** o sistema apresenta todos os motivos de recusa em uma única resposta e preserva os dados atuais.
- **7a. Falha de persistência:** o sistema informa a falha e preserva o arquivo e o estado em memória anteriores à operação.

## UC20 — Consultar Usuário

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Consultar um usuário pelo identificador. |
| Precondições | O Administrador está autenticado e informa o identificador do usuário. |
| Pós-condições | Os dados do usuário são devolvidos sem alteração no repositório. |

### Fluxo principal

1. O Administrador solicita a consulta e informa o identificador do usuário.
2. O sistema busca o usuário pelo identificador.
3. O sistema devolve os dados do usuário encontrado, sem exibir a senha nem seu hash.

### Fluxos alternativos e de exceção

- **2a. Usuário inexistente:** o sistema informa "Usuário com ID '<id>' não encontrado.".

## UC21 — Remover Usuário

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Remover um usuário cadastrado pelo identificador. |
| Precondições | O Administrador está autenticado e informa o identificador de um usuário existente. |
| Pós-condições | O usuário deixa de constar no repositório e a quantidade de usuários é atualizada. |

### Fluxo principal

1. O Administrador seleciona um usuário e solicita a remoção.
2. O sistema localiza o usuário pelo identificador.
3. O sistema remove e persiste o usuário.
4. O sistema confirma a remoção e atualiza a listagem e a contagem de usuários.

### Fluxos alternativos e de exceção

- **2a. Usuário inexistente:** o sistema informa "Usuário com ID '<id>' não encontrado." e não altera o repositório.
- **3a. Falha de persistência:** o sistema informa a falha e preserva o arquivo e o estado em memória anteriores à operação.

## UC12 — Cadastrar Restaurante

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Cadastrar um restaurante parceiro para uso no sistema. |
| Precondições | O Administrador está autenticado e o repositório de restaurantes está disponível. |
| Pós-condições | Um restaurante válido é persistido com identificador, data de cadastro e status `ATIVO`. |

### Fluxo principal

1. O Administrador solicita o cadastro de restaurante.
2. O sistema apresenta nome, descrição, localização, telefone e horário limite de agendamento.
3. O Administrador preenche nome, localização, telefone e horário limite; descrição é opcional.
4. O Administrador confirma os dados.
5. O sistema valida os campos obrigatórios e o horário, reunindo todos os erros encontrados.
6. O sistema remove espaços excedentes das pontas dos textos e cria o restaurante sem ID, com data de cadastro gerada e status `ATIVO`.
7. O repositório atribui o ID e persiste o restaurante; em seguida, o sistema confirma o cadastro.

### Fluxos alternativos e de exceção

- **5a. Dados inválidos:** o sistema informa todos os motivos e não altera a quantidade de restaurantes.
- **7a. Falha de persistência:** o sistema informa a falha, mantém o arquivo e a coleção anteriores intactos e reverte o ID do restaurante para `None`.

## UC16 — Remover Restaurante

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Remover um restaurante que não esteja vinculado a gestores. |
| Precondições | O Administrador está autenticado e informa o identificador do restaurante. |
| Pós-condições | Se a operação for aceita, o restaurante deixa de constar no repositório e a contagem é atualizada. |

### Fluxo principal

1. O Administrador seleciona um restaurante e solicita a remoção.
2. O sistema localiza o restaurante pelo identificador.
3. O sistema verifica se existe algum `GestorRestaurante` associado ao ID.
4. Não havendo gestores vinculados, o sistema remove e persiste a alteração.
5. O sistema confirma a remoção e atualiza a listagem e o resumo de entidades.

### Fluxos alternativos e de exceção

- **2a. Restaurante inexistente:** o sistema recusa a operação e informa que o identificador não foi encontrado.
- **3a. Há gestores vinculados:** o sistema recusa a remoção, informa que há gestores associados e preserva o restaurante.
- **4a. Falha de persistência:** o sistema informa a falha, descarta a operação e preserva o estado anterior.
