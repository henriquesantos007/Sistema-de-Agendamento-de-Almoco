import re
from abc import ABC, abstractmethod
from typing import List

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios


class DadosUsuarioInvalidos(ValueError):
    def __init__(self, erros: List[str]) -> None:
        self.erros = erros
        super().__init__("; ".join(erros))


def normalizar_telefone(telefone: str) -> str:
    return re.sub(r"\D", "", telefone)

class ValidadorUsuarioBase(ABC):
    @abstractmethod
    def validar(self, dados, repositorio) -> List[str]:
        raise NotImplementedError

class ValidadorDadosObrigatorios(ValidadorUsuarioBase):
    def validar(self, dados, repositorio) -> List[str]:
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
    def validar(self, dados, repositorio) -> List[str]:
        erros = []

        email = (dados.email or "").strip()
        if not email:
            return erros

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            erros.append("e-mail invalido")
        elif repositorio.buscar_por_email(email):
            erros.append("e-mail ja cadastrado")

        return erros

class ValidadorPerfil(ValidadorUsuarioBase):
    def validar(self, dados, repositorio) -> List[str]:
        erros = []

        perfil = (dados.perfil or "").strip().lower()
        perfis_validos = {"estudante", "gestor_restaurante", "administrador"}

        if perfil not in perfis_validos:
            erros.append("perfil invalido")

        return erros

class ValidadorEstudante(ValidadorUsuarioBase):
    def validar(self, dados, repositorio) -> List[str]:
        erros = []

        perfil = (dados.perfil or "").strip().lower()
        if perfil != "estudante":
            return erros

        if not dados.matricula or not dados.matricula.strip():
            erros.append("matricula e obrigatoria para estudante")
        elif repositorio.existe_matricula(dados.matricula):
            erros.append("matricula ja cadastrada")

        telefone = re.sub(r"\D", "", dados.telefone or "")
        if telefone and repositorio.existe_telefone(telefone):
            erros.append("telefone ja cadastrado para estudante")

        return erros

class ValidadorGestorRestaurante(ValidadorUsuarioBase):
    def validar(self, dados, repositorio) -> List[str]:
        erros = []

        if (dados.perfil or "").strip().lower() != "gestor_restaurante":
            return erros

        if dados.restaurante_id is None:
            erros.append("restaurante e obrigatorio para gestor")

        return erros

class ValidadorUsuario:
    def __init__(self, validadores):
        self.validadores = validadores

    def validar(self, dados, repositorio) -> List[str]:
        erros = []
        for validador in self.validadores:
            erros.extend(validador.validar(dados, repositorio))
        return erros