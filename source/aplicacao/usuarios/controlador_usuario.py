from typing import List, Optional

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.aplicacao.usuarios.validador_usuario import (
    DadosUsuarioInvalidos,
    ValidadorUsuario,
    normalizar_telefone,
)
from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios
from source.dominio.usuarios.senha import gerar_hash_senha
from source.dominio.usuarios.usuario import (
    Administrador,
    Estudante,
    GestorRestaurante,
    Usuario,
)


class PermissaoNegada(PermissionError):
    pass


class ControladorUsuario:
    # Perfis que só um administrador autenticado pode cadastrar.
    PERFIS_RESTRITOS = {"gestor_restaurante", "administrador"}

    def __init__(
        self,
        repositorio: RepositorioUsuarios,
        validador: Optional[ValidadorUsuario] = None,
    ) -> None:
        self.repositorio = repositorio
        self.validador = validador or ValidadorUsuario(repositorio)

    def cadastrar_usuario(
        self, dados: DadosUsuario, solicitante: Optional[Usuario] = None
    ) -> Usuario:
        perfil = dados.perfil.strip().lower()
        if perfil in self.PERFIS_RESTRITOS and not isinstance(
            solicitante, Administrador
        ):
            raise PermissaoNegada(
                f"apenas administradores podem cadastrar o perfil {perfil}"
            )

        erros = self.validador.validar(dados)
        if erros:
            raise DadosUsuarioInvalidos(erros)

        campos = {
            "nome": dados.nome.strip(),
            "email": dados.email.strip().lower(),
            "senha": gerar_hash_senha(dados.senha),
            "telefone": normalizar_telefone(dados.telefone),
        }

        if perfil == "estudante":
            usuario = Estudante(**campos, matricula=dados.matricula.strip())
        elif perfil == "gestor_restaurante":
            usuario = GestorRestaurante(
                **campos, restaurante_id=dados.restaurante_id
            )
        elif perfil == "administrador":
            usuario = Administrador(**campos)
        else:
            raise DadosUsuarioInvalidos(["perfil invalido"])

        return self.repositorio.adicionar(usuario)

    def listar_usuarios(self) -> List[Usuario]:
        return self.repositorio.listar_todos()
