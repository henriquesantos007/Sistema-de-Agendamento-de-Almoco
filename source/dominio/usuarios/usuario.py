from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional


class StatusUsuario(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    BLOQUEADO = "BLOQUEADO"


class Usuario(ABC):
    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        telefone: str,
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusUsuario = StatusUsuario.ATIVO,
    ) -> None:
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.data_cadastro = data_cadastro or datetime.now()
        self.status = status

    @property
    @abstractmethod
    def perfil(self) -> str:
        raise NotImplementedError


class Estudante(Usuario):
    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        telefone: str,
        matricula: str,
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusUsuario = StatusUsuario.ATIVO,
    ) -> None:
        super().__init__(nome, email, senha, telefone, id, data_cadastro, status)
        self.matricula = matricula

    @property
    def perfil(self) -> str:
        return "estudante"


class GestorRestaurante(Usuario):
    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        telefone: str,
        restaurante_id: int,
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusUsuario = StatusUsuario.ATIVO,
    ) -> None:
        super().__init__(nome, email, senha, telefone, id, data_cadastro, status)
        self.restaurante_id = restaurante_id

    @property
    def perfil(self) -> str:
        return "gestor_restaurante"


class Administrador(Usuario):
    @property
    def perfil(self) -> str:
        return "administrador"