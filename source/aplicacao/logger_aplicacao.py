from abc import ABC, abstractmethod
from enum import Enum


class NivelEvento(Enum):
    INFORMACAO = "informacao"
    AVISO = "aviso"
    ERRO = "erro"


class LoggerAplicacao(ABC):
    """Contrato de logging da aplicacao.

    Controladores e servicos registram eventos operacionais por este contrato,
    sem importar uma biblioteca de logging. As mensagens nao devem conter
    senhas, e-mails ou outros dados pessoais.
    """

    @abstractmethod
    def registrar(
        self,
        evento: str,
        detalhes: str,
        nivel: NivelEvento = NivelEvento.INFORMACAO,
    ) -> None:
        raise NotImplementedError
