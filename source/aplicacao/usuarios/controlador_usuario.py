from copy import deepcopy
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

    def listar_todos(self):
        return self.repositorio.listar_todos()

    def contar(self) -> int:
        return self.repositorio.contar()
    
    def buscar_por_id(self, id_usuario: int):
        usuario = self.repositorio.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError(f"Usuário com ID '{id_usuario}' não encontrado.")
        return usuario

    def atualizar(self, id_usuario: int, dados_atualizados):
        usuario_existente = self.buscar_por_id(id_usuario)
        
        erros = self.validador_usuario.validar(
            dados=dados_atualizados, 
            repositorio = self.repositorio,
            id_ignorado = id_usuario
        )
        
        if erros:
            raise ValueError(f"Erros de validação: {', '.join(erros)}")
            
        # Persiste uma cópia para que falhas de armazenamento não alterem a
        # entidade atualmente mantida pelo repositório.
        usuario_atualizado = deepcopy(usuario_existente)
        usuario_atualizado.nome = dados_atualizados.nome
        usuario_atualizado.email = dados_atualizados.email
        usuario_atualizado.senha = gerar_hash_senha(dados_atualizados.senha)
        usuario_atualizado.login = (dados_atualizados.login or "").strip()
        usuario_atualizado.telefone = normalizar_telefone(
            dados_atualizados.telefone
        )

        return self.repositorio.atualizar(usuario_atualizado)

    def remover(self, id_usuario: int):
        self.buscar_por_id(id_usuario)
        
        self.repositorio.remover(id_usuario)