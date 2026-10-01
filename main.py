from source.aplicacao.usuarios import ControladorUsuario, DadosUsuario
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria


def main():
    controlador = ControladorUsuario(RepositorioUsuariosMemoria())
    dados_usuario = DadosUsuario(
        "estudante",
        "Ana Silva",
        "ana@example.com",
        "senha",
        "83999990000",
        "2026001",
    )
    controlador.cadastrar_usuario(dados_usuario)
    print(
        [
            (usuario.id, usuario.perfil, usuario.email, usuario.status.value)
            for usuario in controlador.listar_usuarios()
        ]
    )


if __name__ == "__main__":
    main()