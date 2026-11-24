from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from source.dominio.usuarios.perfil import Perfil


class StatusUsuario(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    BLOQUEADO = "BLOQUEADO"


@dataclass
class DadosBasicosUsuario:
    nome: str
    login: str
    email: str
    senha: str
    telefone: str
    id: Optional[int] = None
    data_cadastro: Optional[datetime] = None
    status: StatusUsuario = StatusUsuario.ATIVO


class Usuario(ABC):
    def __init__(self, dados: DadosBasicosUsuario) -> None:
        self.id = dados.id
        self.nome = dados.nome
        self.login = dados.login
        self.email = dados.email
        self.senha = dados.senha
        self.telefone = dados.telefone
        self.data_cadastro = dados.data_cadastro or datetime.now()
        self.status = dados.status

    @property
    @abstractmethod
    def perfil(self) -> str:
        raise NotImplementedError


class Estudante(Usuario):
    def __init__(self, dados: DadosBasicosUsuario, matricula: str) -> None:
        super().__init__(dados)
        self.matricula = matricula

    @property
    def perfil(self) -> str:
        return Perfil.ESTUDANTE.value


class GestorRestaurante(Usuario):
    def __init__(self, dados: DadosBasicosUsuario, restaurante_id: int) -> None:
        super().__init__(dados)
        self.restaurante_id = restaurante_id

    @property
    def perfil(self) -> str:
        return Perfil.GESTOR_RESTAURANTE.value


class Administrador(Usuario):
    @property
    def perfil(self) -> str:
        return Perfil.ADMINISTRADOR.value
