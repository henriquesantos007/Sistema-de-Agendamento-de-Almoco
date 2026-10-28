# Casos de Uso Detalhados

Este documento detalha os três casos de uso selecionados para a entrega:
**UC05 — Cadastrar Usuário**, **UC12 — Cadastrar Restaurante** e
**UC16 — Remover Restaurante**. Os atores, precondições e fluxos seguem as
regras de [usuários](../../openspec/specs/usuarios/spec.md) e
[restaurantes](../../openspec/specs/restaurantes/spec.md).

## UC05 — Cadastrar Usuário

| Campo | Descrição |
|---|---|
| Ator principal | Administrador |
| Objetivo | Registrar uma conta de usuário com um perfil válido. |
| Precondições | O Administrador está autenticado. Para o perfil Gestor de Restaurante, o restaurante a vincular já está cadastrado. |
| Pós-condições | O usuário validado é persistido com identificador gerado; sua senha fica armazenada somente como hash. |

### Fluxo principal

1. O Administrador inicia o cadastro e escolhe Estudante, Gestor de Restaurante ou Administrador.
2. O sistema apresenta os campos comuns: nome, login, e-mail, senha e telefone.
3. O Administrador informa os dados e, conforme o perfil, a matrícula do Estudante ou o restaurante do Gestor.
4. O Administrador confirma o cadastro.
5. O sistema valida os campos, as regras de login e senha, os dados únicos e o vínculo do Gestor.
6. O sistema normaliza os campos textuais, gera o hash da senha e cria o usuário com identificador.
7. O sistema persiste o usuário e confirma o cadastro, sem exibir a senha nem seu hash.

### Fluxos alternativos e de exceção

- **5a. Dados inválidos ou duplicados:** o sistema reúne e apresenta todos os motivos; nenhum usuário é cadastrado.
- **5b. Perfil Estudante sem matrícula:** o sistema informa que a matrícula é obrigatória e mantém o cadastro inalterado.
- **5c. Perfil Gestor sem restaurante ou com ID inexistente:** o sistema informa o motivo e não cria o usuário.
- **7a. Falha de persistência:** o sistema informa a falha e descarta a operação, preservando os dados anteriores.

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
6. O sistema remove espaços excedentes das pontas dos textos, cria o restaurante com ID e data gerados e status `ATIVO`.
7. O sistema persiste o restaurante e confirma o cadastro.

### Fluxos alternativos e de exceção

- **5a. Dados inválidos:** o sistema informa todos os motivos e não altera a quantidade de restaurantes.
- **7a. Falha de persistência:** o sistema informa a falha e mantém o arquivo e a coleção anteriores intactos.

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
