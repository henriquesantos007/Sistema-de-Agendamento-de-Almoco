from source.aplicacao.usuarios import (
    ControladorUsuario,
    DadosUsuario,
    DadosUsuarioInvalidos,
)
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria
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

def main():
    validador = ValidadorUsuario([
        ValidadorDadosObrigatorios(),
        ValidadorPerfil(),
        ValidadorLogin(),
        ValidadorEmail(),
        ValidadorSenha(),
        ValidadorEstudante(),
        ValidadorGestorRestaurante(),
    ])

    repositorio = RepositorioUsuariosMemoria()

    controlador = ControladorUsuario(repositorio, validador)

    dados_usuario = DadosUsuario(
        perfil="estudante",
        nome="Ana Silva",
        login="anasilva",
        email="ana@example.com",
        senha="Senha@2026",
        telefone="83999990000",
        matricula="2026001",
    )

    usuario = controlador.cadastrar(dados_usuario)
    print(usuario)
    print(repositorio.listar_todos())

    # Exemplo de tratamento de erros: login e senha fora das regras
    dados_invalidos = DadosUsuario(
        perfil="estudante",
        nome="Bruno Lima",
        login="bruno123456789",
        email="bruno@example.com",
        senha="curta",
        telefone="83988880000",
        matricula="2026002",
    )

    try:
        controlador.cadastrar(dados_invalidos)
    except DadosUsuarioInvalidos as erro:
        print("Cadastro recusado:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")


if __name__ == "__main__":
    main()