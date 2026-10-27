from abc import ABC, abstractmethod
from typing import List, Optional

from source.dominio.restaurantes.restaurante import Restaurante


class RepositorioRestaurantes(ABC):
    @abstractmethod
    def adicionar(self, restaurante: Restaurante) -> Restaurante:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, restaurante_id: int) -> Optional[Restaurante]:
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> List[Restaurante]:
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, restaurante: Restaurante) -> Restaurante:
        raise NotImplementedError

    @abstractmethod
    def remover(self, restaurante_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def contar(self) -> int:
        raise NotImplementedError
