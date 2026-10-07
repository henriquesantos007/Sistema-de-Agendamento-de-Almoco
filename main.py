from source.aplicacao.usuarios import ControladorUsuario, DadosUsuario
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria
from source.aplicacao.usuarios.validador_usuario import (
    ValidadorUsuario,
    ValidadorDadosObrigatorios,
    ValidadorPerfil,
    ValidadorEmail,
    ValidadorEstudante,
    ValidadorGestorRestaurante,
)

def main():
    validador = ValidadorUsuario([
    ValidadorDadosObrigatorios(),
    ValidadorPerfil(),
    ValidadorEmail(),
    ValidadorEstudante(),
    ValidadorGestorRestaurante(),
    ])

    repositorio = RepositorioUsuariosMemoria()

    controlador = ControladorUsuario(repositorio, validador)

    dados_usuario = DadosUsuario(
        "estudante",
        "Ana Silva",
        "ana@example.com",
        "senha",
        "83999990000",
        "2026001",
    )

    usuario = controlador.cadastrar(dados_usuario)
    print(usuario)
    print(repositorio.listar_todos())


if __name__ == "__main__":
    main()