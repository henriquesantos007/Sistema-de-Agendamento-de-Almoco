import pytest

from source.aplicacao.logger_aplicacao import NivelEvento
from source.aplicacao.relatorios import (
    FORMATOS_ACEITOS,
    FormatoRelatorioInvalido,
    RelatorioAcessoCSV,
    RelatorioAcessoHTML,
    ServicoRelatorioAcesso,
)
from source.dominio.acessos import ErroPersistencia
from tests.apoio_relatorios import (
    LoggerEmMemoria,
    UsuariosCadastrados,
    acessos_de,
    administrador,
    estudante,
)


class AcessosIndisponiveis:
    def listar_todos(self):
        raise ErroPersistencia("nao foi possivel ler o arquivo 'acessos.jsonl'")


class AcessosQueNaoDevemSerConsultados:
    def listar_todos(self):
        raise AssertionError("os registros nao deveriam ser consultados")


@pytest.fixture
def logger():
    return LoggerEmMemoria()


@pytest.fixture
def servico(logger):
    return ServicoRelatorioAcesso(
        acessos_de(1, 2, 1),
        UsuariosCadastrados([estudante(1, "ana"), administrador(2, "bruno")]),
        logger,
    )


def test_formatos_aceitos_devem_ser_html_e_csv():
    assert FORMATOS_ACEITOS == ("HTML", "CSV")


@pytest.mark.parametrize(
    "formato, classe",
    [("html", RelatorioAcessoHTML), ("csv", RelatorioAcessoCSV)],
)
def test_deve_gerar_o_documento_do_formato_pedido(servico, formato, classe):
    acessos = acessos_de(1, 2, 1)
    usuarios = UsuariosCadastrados([estudante(1, "ana"), administrador(2, "bruno")])

    documento = servico.gerar(formato)

    assert documento == classe(acessos, usuarios).gerar()


@pytest.mark.parametrize("formato", ["HTML", " Html ", "CSV", "csv\n"])
def test_formato_deve_ignorar_caixa_e_espacos(servico, formato):
    assert servico.gerar(formato).formato == formato.strip().lower()


@pytest.mark.parametrize("formato", ["PDF", "", "htm", None, 1])
def test_formato_nao_suportado_deve_ser_recusado(servico, formato):
    with pytest.raises(FormatoRelatorioInvalido) as excecao:
        servico.gerar(formato)

    assert isinstance(excecao.value, ValueError)
    assert excecao.value.formatos_aceitos == ["HTML", "CSV"]
    assert "HTML e CSV" in str(excecao.value)


def test_recusa_deve_acontecer_antes_de_qualquer_consulta(logger):
    servico = ServicoRelatorioAcesso(
        AcessosQueNaoDevemSerConsultados(), UsuariosCadastrados([]), logger
    )

    with pytest.raises(FormatoRelatorioInvalido):
        servico.gerar("PDF")


def test_geracao_deve_registrar_formato_e_resultado(servico, logger):
    servico.gerar("CSV")

    assert logger.eventos == [
        (
            "relatorio_acessos_gerado",
            "formato=csv; relatorio gerado",
            NivelEvento.INFORMACAO,
        )
    ]


def test_recusa_de_formato_deve_ser_registrada(servico, logger):
    with pytest.raises(FormatoRelatorioInvalido):
        servico.gerar("PDF")

    assert logger.eventos == [
        (
            "relatorio_acessos_recusado",
            "formato nao suportado; formatos aceitos: HTML, CSV",
            NivelEvento.AVISO,
        )
    ]


def test_falha_de_persistencia_deve_ser_registrada_e_repassada(logger):
    servico = ServicoRelatorioAcesso(
        AcessosIndisponiveis(), UsuariosCadastrados([]), logger
    )

    with pytest.raises(ErroPersistencia):
        servico.gerar("html")

    assert logger.eventos == [
        (
            "relatorio_acessos_falhou",
            "formato=html; falha de persistencia",
            NivelEvento.ERRO,
        )
    ]


@pytest.mark.parametrize("formato", ["html", "csv", "PDF ana@example.com"])
def test_eventos_nao_devem_conter_dados_pessoais(servico, logger, formato):
    try:
        servico.gerar(formato)
    except FormatoRelatorioInvalido:
        pass

    mensagens = " ".join(f"{evento} {detalhes}" for evento, detalhes, _ in logger.eventos)
    for dado_pessoal in ("ana", "bruno", "example.com", "Senha@2026", "8399999"):
        assert dado_pessoal not in mensagens
