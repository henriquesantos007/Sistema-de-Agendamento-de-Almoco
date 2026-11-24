from abc import ABC, abstractmethod


class Comando(ABC):
    """Interface base para o padrão Command."""

    @abstractmethod
    def executar(self):
        """Executa a ação encapsulada pelo comando."""
        raise NotImplementedError

    @abstractmethod
    def desfazer(self):
        """Desfaz a ação executada, restaurando o estado anterior."""
        raise NotImplementedError