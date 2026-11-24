from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional
from source.dominio.usuarios.memento import UsuarioMemento


class StatusUsuario(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    BLOQUEADO = "BLOQUEADO"


class Usuario(ABC):
    def __init__(
        self,
        nome: str,
        login: str,
        email: str,
        senha: str,
        telefone: str,
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusUsuario = StatusUsuario.ATIVO,
    ) -> None:
        self.id = id
        self.nome = nome
        self.login = login
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.data_cadastro = data_cadastro or datetime.now()
        self.status = status

    @property
    @abstractmethod
    def perfil(self) -> str:
        raise NotImplementedError

    def criar_memento(self) -> UsuarioMemento:
        """Cria um memento contendo o snapshot de seu estado atual."""
        # Captura todos os atributos atuais do objeto dinamicamente
        return UsuarioMemento(self.__dict__)

    def restaurar_memento(self, memento: UsuarioMemento) -> None:
        """Usa o Memento para restaurar seu estado interno original."""
        estado_restaurado = memento.get_estado()
        self.__dict__.update(estado_restaurado)


class Estudante(Usuario):
    def __init__(
        self,
        nome: str,
        login: str,
        email: str,
        senha: str,
        telefone: str,
        matricula: str,
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusUsuario = StatusUsuario.ATIVO,
    ) -> None:
        super().__init__(
            nome, login, email, senha, telefone, id, data_cadastro, status
        )
        self.matricula = matricula

    @property
    def perfil(self) -> str:
        return "estudante"


class GestorRestaurante(Usuario):
    def __init__(
        self,
        nome: str,
        login: str,
        email: str,
        senha: str,
        telefone: str,
        restaurante_id: int,
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusUsuario = StatusUsuario.ATIVO,
    ) -> None:
        super().__init__(
            nome, login, email, senha, telefone, id, data_cadastro, status
        )
        self.restaurante_id = restaurante_id

    @property
    def perfil(self) -> str:
        return "gestor_restaurante"


class Administrador(Usuario):
    @property
    def perfil(self) -> str:
        return "administrador"