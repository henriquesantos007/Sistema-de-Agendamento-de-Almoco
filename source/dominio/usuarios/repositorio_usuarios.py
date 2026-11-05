from abc import ABC, abstractmethod
from typing import List, Optional

from source.dominio.usuarios.usuario import Usuario


class RepositorioUsuarios(ABC):
    @abstractmethod
    def adicionar(self, usuario: Usuario) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def existe_login(self, login: str, id_ignorado: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def existe_matricula(self, matricula: str, id_ignorado: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def existe_telefone(self, telefone: str, id_ignorado: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    def contar(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def atualizar(self, usuario_atualizado: Usuario) -> Usuario:
        pass

    @abstractmethod
    def remover(self, id_usuario: int) -> None:
        pass
