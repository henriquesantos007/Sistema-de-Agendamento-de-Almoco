from typing import List, Optional

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.aplicacao.usuarios.excecoes import DadosUsuarioInvalidos
from source.aplicacao.usuarios.fabrica_usuario import FabricaUsuario
from source.dominio.usuarios.perfil import Perfil
from source.dominio.usuarios.senha import gerar_hash_senha
from source.dominio.usuarios.telefone import normalizar_telefone
from source.dominio.usuarios.usuario import DadosBasicosUsuario, Usuario


class ControladorUsuario:
    def __init__(self, repositorio, validador_usuario, fabrica=None):
        self.repositorio = repositorio
        self.validador_usuario = validador_usuario
        self.fabrica = fabrica or FabricaUsuario()

    def cadastrar(self, dados):
        erros = self.validador_usuario.validar(dados, self.repositorio)

        if erros:
            raise DadosUsuarioInvalidos(erros)

        usuario = self._criar_usuario(dados)
        self.repositorio.adicionar(usuario)
        return usuario

    def _criar_usuario(self, dados: DadosUsuario) -> Usuario:
        perfil = Perfil.de_texto(dados.perfil)
        if perfil is None:
            raise ValueError("perfil invalido")

        basicos = DadosBasicosUsuario(
            nome=dados.nome,
            login=(dados.login or "").strip(),
            email=dados.email,
            senha=gerar_hash_senha(dados.senha),
            telefone=normalizar_telefone(dados.telefone),
        )
        return self.fabrica.criar(perfil, basicos, dados)

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
            
        # Transfere os dados validados do DTO para a Entidade Existente
        usuario_existente.nome = dados_atualizados.nome
        usuario_existente.email = dados_atualizados.email
        usuario_existente.senha = dados_atualizados.senha
        usuario_existente.login = dados_atualizados.login
        usuario_existente.telefone = dados_atualizados.telefone
        
        return self.repositorio.atualizar(usuario_existente)

    def remover(self, id_usuario: int):
        self.buscar_por_id(id_usuario)
        
        self.repositorio.remover(id_usuario)