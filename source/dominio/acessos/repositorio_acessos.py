from abc import ABC, abstractmethod
from typing import List

from source.dominio.acessos.registro_acesso import RegistroAcesso


class RepositorioAcessos(ABC):
    """Registros de acesso sao imutaveis: so e possivel registrar e listar."""

    @abstractmethod
    def registrar(self, acesso: RegistroAcesso) -> None:
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> List[RegistroAcesso]:
        raise NotImplementedError
