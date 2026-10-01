from abc import ABC, abstractmethod
from typing import List, Optional

from source.dominio.usuarios.usuario import Usuario


class RepositorioUsuarios(ABC):
    @abstractmethod
    def adicionar(self, usuario: Usuario) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def existe_matricula(self, matricula: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def existe_telefone(self, telefone: str) -> bool:
        raise NotImplementedError