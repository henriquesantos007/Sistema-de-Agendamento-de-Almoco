import logging

import pytest

from source.aplicacao.logger_aplicacao import LoggerAplicacao, NivelEvento
from source.infraestrutura.logs import (
    NOME_LOGGER,
    AdaptadorLogging,
    criar_adaptador_logging,
)


@pytest.fixture
def logger_isolado():
    logger = logging.getLogger("teste.adaptador_logging")
    yield logger
    logger.handlers.clear()


def test_contrato_nao_deve_ser_instanciado():
    with pytest.raises(TypeError):
        LoggerAplicacao()


def test_adaptador_deve_implementar_o_contrato_da_aplicacao(logger_isolado):
    assert isinstance(AdaptadorLogging(logger_isolado), LoggerAplicacao)


def test_deve_delegar_o_evento_a_biblioteca_logging(logger_isolado, caplog):
    adaptador = AdaptadorLogging(logger_isolado)

    with caplog.at_level(logging.DEBUG, logger=logger_isolado.name):
        adaptador.registrar("relatorio_acessos_gerado", "formato=csv")

    registro = caplog.records[0]
    assert registro.name == logger_isolado.name
    assert registro.levelno == logging.INFO
    assert registro.getMessage() == "relatorio_acessos_gerado | formato=csv"


@pytest.mark.parametrize(
    "nivel, nivel_da_biblioteca",
    [
        (NivelEvento.INFORMACAO, logging.INFO),
        (NivelEvento.AVISO, logging.WARNING),
        (NivelEvento.ERRO, logging.ERROR),
    ],
)
def test_deve_converter_o_nivel_do_evento(
    logger_isolado, caplog, nivel, nivel_da_biblioteca
):
    adaptador = AdaptadorLogging(logger_isolado)

    with caplog.at_level(logging.DEBUG, logger=logger_isolado.name):
        adaptador.registrar("evento", "detalhes", nivel)

    assert caplog.records[0].levelno == nivel_da_biblioteca


def test_evento_com_porcentagem_nao_deve_ser_tratado_como_formato(
    logger_isolado, caplog
):
    adaptador = AdaptadorLogging(logger_isolado)

    with caplog.at_level(logging.DEBUG, logger=logger_isolado.name):
        adaptador.registrar("evento %s", "100% %d")

    assert caplog.records[0].getMessage() == "evento %s | 100% %d"


def test_criar_adaptador_deve_configurar_o_logger_da_aplicacao_uma_unica_vez():
    logger = logging.getLogger(NOME_LOGGER)
    handlers_anteriores = list(logger.handlers)
    logger.handlers.clear()
    try:
        primeiro = criar_adaptador_logging()
        segundo = criar_adaptador_logging()

        assert isinstance(primeiro, AdaptadorLogging)
        assert isinstance(segundo, AdaptadorLogging)
        assert len(logger.handlers) == 1
        assert logger.level == logging.INFO
    finally:
        logger.handlers[:] = handlers_anteriores
