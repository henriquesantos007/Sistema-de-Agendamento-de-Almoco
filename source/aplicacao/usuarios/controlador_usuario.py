from typing import List, Optional

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.aplicacao.usuarios.validador_usuario import (
    DadosUsuarioInvalidos,
    ValidadorUsuario,
)
from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios
from source.dominio.usuarios.usuario import (
    Administrador,
    Estudante,
    GestorRestaurante,
    Usuario,
)


class ControladorUsuario:
    def __init__(
        self,
        repositorio: RepositorioUsuarios,
        validador: Optional[ValidadorUsuario] = None,
    ) -> None:
        self.repositorio = repositorio
        self.validador = validador or ValidadorUsuario(repositorio)

    def cadastrar_usuario(self, dados: DadosUsuario) -> Usuario:
        erros = self.validador.validar(dados)
        if erros:
            raise DadosUsuarioInvalidos(erros)

        campos = {
            "nome": dados.nome.strip(),
            "email": dados.email.strip().lower(),
            "senha": dados.senha,
            "telefone": dados.telefone.strip(),
        }
        perfil = dados.perfil.strip().lower()

        if perfil == "estudante":
            usuario = Estudante(**campos, matricula=dados.matricula.strip())
        elif perfil == "gestor_restaurante":
            usuario = GestorRestaurante(
                **campos, restaurante_id=dados.restaurante_id
            )
        else:
            usuario = Administrador(**campos)

        return self.repositorio.adicionar(usuario)

