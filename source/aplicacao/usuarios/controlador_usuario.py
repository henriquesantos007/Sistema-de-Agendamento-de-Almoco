from typing import List, Optional

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.aplicacao.usuarios.excecoes import DadosUsuarioInvalidos
from source.aplicacao.usuarios.validador_usuario import normalizar_telefone
from source.dominio.usuarios.senha import gerar_hash_senha
from source.dominio.usuarios.usuario import (
    Administrador,
    Estudante,
    GestorRestaurante,
    Usuario,
)


class ControladorUsuario:
    def __init__(self, repositorio, validador_usuario):
        self.repositorio = repositorio
        self.validador_usuario = validador_usuario

    def cadastrar(self, dados):
        erros = self.validador_usuario.validar(dados, self.repositorio)

        if erros:
            raise DadosUsuarioInvalidos(erros)

        usuario = self._criar_usuario(dados)
        self.repositorio.adicionar(usuario)
        return usuario

    def _criar_usuario(self, dados: DadosUsuario) -> Usuario:
        perfil = (dados.perfil or "").strip().lower()

        login = (dados.login or "").strip()
        senha_hash = gerar_hash_senha(dados.senha)
        telefone_normalizado = normalizar_telefone(dados.telefone)

        if perfil == "estudante":
            return Estudante(
                nome=dados.nome,
                login=login,
                email=dados.email,
                senha=senha_hash,
                telefone=telefone_normalizado,
                matricula=dados.matricula or "",
            )

        if perfil == "gestor_restaurante":
            return GestorRestaurante(
                nome=dados.nome,
                login=login,
                email=dados.email,
                senha=senha_hash,
                telefone=telefone_normalizado,
                restaurante_id=dados.restaurante_id,
            )

        if perfil == "administrador":
            return Administrador(
                nome=dados.nome,
                login=login,
                email=dados.email,
                senha=senha_hash,
                telefone=telefone_normalizado,
            )

        raise ValueError("perfil invalido")