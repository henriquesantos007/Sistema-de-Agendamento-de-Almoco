import argparse

from source.aplicacao.usuarios import (
    ControladorUsuario,
    DadosUsuario,
    DadosUsuarioInvalidos,
)
from source.aplicacao.usuarios.validador_usuario import (
    ValidadorUsuario,
    ValidadorDadosObrigatorios,
    ValidadorPerfil,
    ValidadorLogin,
    ValidadorEmail,
    ValidadorSenha,
    ValidadorEstudante,
    ValidadorGestorRestaurante,
)
from source.dominio.usuarios import ErroPersistencia
from source.infraestrutura.persistencia.fabrica_repositorio import (
    ARMAZENAMENTOS,
    criar_repositorio_usuarios
)


def ler_argumentos():
    parser = argparse.ArgumentParser(description="Cadastro de usuarios")
    parser.add_argument(
        "--armazenamento",
        choices=ARMAZENAMENTOS,
        default="memoria",
        help="mecanismo de persistencia (padrao: memoria)",
    )
    parser.add_argument(
        "--caminho",
        default=None,
        help="arquivo do armazenamento (padrao: dados/usuarios.bin)",
    )
    return parser.parse_args()


def tentar_cadastrar(controlador, dados):
    try:
        usuario = controlador.cadastrar(dados)
        print(f"Cadastrado: {usuario.perfil} '{usuario.login}' (id={usuario.id})")
    except DadosUsuarioInvalidos as erro:
        print(f"Cadastro de '{dados.login}' recusado:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")
    except ErroPersistencia as erro:
        print(f"Falha de persistencia ao cadastrar '{dados.login}': {erro}")


def main():
    argumentos = ler_argumentos()

    try:
        repositorio = criar_repositorio_usuarios(
            argumentos.armazenamento, argumentos.caminho
        )
    except ErroPersistencia as erro:
        print(f"Nao foi possivel iniciar o armazenamento: {erro}")
        return

    validador = ValidadorUsuario([
        ValidadorDadosObrigatorios(),
        ValidadorPerfil(),
        ValidadorLogin(),
        ValidadorEmail(),
        ValidadorSenha(),
        ValidadorEstudante(),
        ValidadorGestorRestaurante(),
    ])

    controlador = ControladorUsuario(repositorio, validador)

    print(f"Armazenamento: {argumentos.armazenamento}")

    tentar_cadastrar(controlador, DadosUsuario(
        perfil="estudante",
        nome="Ana Silva",
        login="anasilva",
        email="ana@example.com",
        senha="Senha@2026",
        telefone="83999990000",
        matricula="2026001",
    ))

    # Exemplo de tratamento de erros: login e senha fora das regras
    tentar_cadastrar(controlador, DadosUsuario(
        perfil="estudante",
        nome="Bruno Lima",
        login="bruno123456789",
        email="bruno@example.com",
        senha="curta",
        telefone="83988880000",
        matricula="2026002",
    ))

    try:
        usuarios = repositorio.listar_todos()
    except ErroPersistencia as erro:
        print(f"Falha de persistencia ao listar usuarios: {erro}")
        return

    print("Usuarios armazenados:")
    for usuario in usuarios:
        print(f"  [{usuario.id}] {usuario.perfil} | {usuario.login} | {usuario.email}")


if __name__ == "__main__":
    main()