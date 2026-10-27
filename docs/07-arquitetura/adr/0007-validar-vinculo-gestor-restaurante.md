# ADR-0007: Validar vínculo entre gestor e restaurante

- Status: Aceito
- Data: 2026-10-27

## Contexto

`GestorRestaurante` armazena `restaurante_id`. Sem validar a referência no
cadastro, o sistema pode guardar um gestor apontando para um restaurante
inexistente. A remoção de um restaurante já referenciado também deixaria o
vínculo inválido.

## Decisão

Injetar `RepositorioRestaurantes` em `ValidadorGestorRestaurante` e recusar o
cadastro de gestores quando o ID não existir. Injetar `RepositorioUsuarios` em
`ControladorRestaurante` e recusar a remoção quando algum usuário do tipo
`GestorRestaurante` referenciar esse ID. A remoção de um restaurante inexistente
continua retornando `False`.

O `main.py` cria o repositório de restaurantes com o mesmo mecanismo de
armazenamento selecionado para usuários, usando o caminho padrão independente
`dados/restaurantes.bin`.

## Consequências

- O cadastro de gestores depende de um repositório de restaurantes configurado.
- O controlador de restaurantes depende também do repositório de usuários.
- Os contratos públicos dos construtores mudam e seus chamadores devem fornecer
  essas dependências.
- Não é possível remover restaurantes que ainda estejam associados a gestores.
