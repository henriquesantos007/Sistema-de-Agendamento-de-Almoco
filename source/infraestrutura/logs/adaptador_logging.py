import logging
from typing import Optional

from source.aplicacao.logger_aplicacao import LoggerAplicacao, NivelEvento

NOME_LOGGER = "agendamento_almoco"

_FORMATO_SAIDA = "%(asctime)s %(levelname)s %(name)s: %(message)s"

_NIVEIS = {
    NivelEvento.INFORMACAO: logging.INFO,
    NivelEvento.AVISO: logging.WARNING,
    NivelEvento.ERRO: logging.ERROR,
}


class AdaptadorLogging(LoggerAplicacao):
    """Adapter do contrato LoggerAplicacao para o modulo logging padrao."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger or logging.getLogger(NOME_LOGGER)

    def registrar(
        self,
        evento: str,
        detalhes: str,
        nivel: NivelEvento = NivelEvento.INFORMACAO,
    ) -> None:
        self._logger.log(_NIVEIS[nivel], "%s | %s", evento, detalhes)


def criar_adaptador_logging() -> AdaptadorLogging:
    """Configura a saida do logger da aplicacao e devolve o Adapter."""
    logger = logging.getLogger(NOME_LOGGER)
    if not logger.handlers:
        saida = logging.StreamHandler()
        saida.setFormatter(logging.Formatter(_FORMATO_SAIDA))
        logger.addHandler(saida)
    logger.setLevel(logging.INFO)
    return AdaptadorLogging(logger)
