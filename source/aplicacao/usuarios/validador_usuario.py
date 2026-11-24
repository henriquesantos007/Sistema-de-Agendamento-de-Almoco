import re
from abc import ABC, abstractmethod
from typing import List

from source.dominio.usuarios.excecoes import LoginInvalido, SenhaInvalida
from source.dominio.usuarios.perfil import Perfil
from source.dominio.usuarios.politica_credenciais import (
    validar_login,
    validar_senha,
)
from source.dominio.restaurantes.repositorio_restaurantes import (
    RepositorioRestaurantes,
)
from source.dominio.usuarios.telefone import normalizar_telefone

class ValidadorUsuarioBase(ABC):
    @abstractmethod
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        raise NotImplementedError

class ValidadorDadosObrigatorios(ValidadorUsuarioBase):
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        erros = []

        campos = {
            "nome": dados.nome,
            "email": dados.email,
            "senha": dados.senha,
            "telefone": dados.telefone,
        }

        for campo, valor in campos.items():
            if not valor or not valor.strip():
                erros.append(f"{campo} e obrigatorio")

        return erros

class ValidadorEmail(ValidadorUsuarioBase):
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        erros = []

        email = (dados.email or "").strip()
        if not email:
            return erros

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            erros.append("e-mail invalido")
        elif repositorio.buscar_por_email(email):
            usuario_existente = repositorio.buscar_por_email(email)
            
            if usuario_existente and usuario_existente.id != id_ignorado:
                erros.append("e-mail ja cadastrado")

        return erros

class ValidadorPerfil(ValidadorUsuarioBase):
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        erros = []

        if Perfil.de_texto(dados.perfil) is None:
            erros.append("perfil invalido")

        return erros

class ValidadorEstudante(ValidadorUsuarioBase):
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        erros = []

        if Perfil.de_texto(dados.perfil) is not Perfil.ESTUDANTE:
            return erros

        if not dados.matricula or not dados.matricula.strip():
            erros.append("matricula e obrigatoria para estudante")
        elif repositorio.existe_matricula(dados.matricula, id_ignorado):
            erros.append("matricula ja cadastrada")

        telefone = normalizar_telefone(dados.telefone or "")
        if telefone and repositorio.existe_telefone(telefone, id_ignorado):
            erros.append("telefone ja cadastrado para estudante")

        return erros

class ValidadorGestorRestaurante(ValidadorUsuarioBase):
    def __init__(self, repositorio_restaurantes: RepositorioRestaurantes) -> None:
        self.repositorio_restaurantes = repositorio_restaurantes

    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        erros = []

        if Perfil.de_texto(dados.perfil) is not Perfil.GESTOR_RESTAURANTE:
            return erros

        if dados.restaurante_id is None:
            erros.append("restaurante e obrigatorio para gestor")
        elif self.repositorio_restaurantes.buscar_por_id(dados.restaurante_id) is None:
            erros.append("restaurante nao encontrado")

        return erros

class ValidadorLogin(ValidadorUsuarioBase):
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        try:
            login = validar_login(dados.login)
        except LoginInvalido as erro:
            return list(erro.motivos)

        if repositorio.existe_login(login, id_ignorado):
            return ["login ja cadastrado"]
        return []

class ValidadorSenha(ValidadorUsuarioBase):
    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        senha = dados.senha
        # Senha vazia ja e reportada por ValidadorDadosObrigatorios.
        if not senha or not senha.strip():
            return []

        try:
            validar_senha(senha, login=dados.login, email=dados.email)
        except SenhaInvalida as erro:
            return list(erro.motivos)
        return []

class ValidadorUsuario:
    def __init__(self, validadores):
        self.validadores = validadores

    def validar(self, dados, repositorio, id_ignorado: int = None) -> List[str]:
        erros = []
        for validador in self.validadores:
            erros.extend(validador.validar(dados, repositorio, id_ignorado))
        return erros