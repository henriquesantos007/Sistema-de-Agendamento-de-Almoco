import csv
import io
from html.parser import HTMLParser
from typing import List

import pytest

from source.aplicacao.relatorios import (
    USUARIO_REMOVIDO,
    RelatorioAcessoCSV,
    RelatorioAcessoHTML,
    TemplateRelatorioAcesso,
)
from tests.apoio_relatorios import (
    UsuariosCadastrados,
    acessos_de,
    administrador,
    estudante,
)


class LeitorDeTabelas(HTMLParser):
    """Extrai o texto das celulas de cada tabela, agrupado pelo id da tabela."""

    def __init__(self) -> None:
        super().__init__()
        self.tabelas = {}
        self._tabela = None
        self._linha = None
        self._celula = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._tabela = self.tabelas.setdefault(dict(attrs)["id"], [])
        elif tag == "tr":
            self._linha = []
        elif tag in ("td", "th"):
            self._celula = ""

    def handle_data(self, data):
        if self._celula is not None:
            self._celula += data

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self._linha.append(self._celula)
            self._celula = None
        elif tag == "tr":
            self._tabela.append(self._linha)
            self._linha = None


def tabelas_do_html(conteudo: str) -> dict:
    leitor = LeitorDeTabelas()
    leitor.feed(conteudo)
    return leitor.tabelas


def blocos_do_csv(conteudo: str) -> List[List[List[str]]]:
    blocos = [[]]
    for linha in csv.reader(io.StringIO(conteudo)):
        if linha:
            blocos[-1].append(linha)
        else:
            blocos.append([])
    return blocos


@pytest.fixture
def repositorios():
    acessos = acessos_de(1, 2, 1, 2, 1, 7)
    usuarios = UsuariosCadastrados(
        [estudante(1, "ana"), administrador(2, "bruno")]
    )
    return acessos, usuarios


LINHAS_ESPERADAS = [
    ["1", "ana", "estudante", "3"],
    ["2", "bruno", "administrador", "2"],
    ["7", USUARIO_REMOVIDO, USUARIO_REMOVIDO, "1"],
]


@pytest.mark.parametrize("formato", [RelatorioAcessoHTML, RelatorioAcessoCSV])
def test_formatos_devem_especializar_o_template(formato, repositorios):
    assert isinstance(formato(*repositorios), TemplateRelatorioAcesso)


def test_html_deve_apresentar_resumo_e_detalhamento(repositorios):
    documento = RelatorioAcessoHTML(*repositorios).gerar()

    tabelas = tabelas_do_html(documento.conteudo)
    assert documento.formato == "html"
    assert documento.conteudo.startswith("<!DOCTYPE html>")
    assert tabelas["resumo"] == [
        ["Total de acessos", "6"],
        ["Usuários distintos", "3"],
    ]
    assert tabelas["detalhamento"][0] == ["Id", "Login", "Perfil", "Acessos"]
    assert tabelas["detalhamento"][1:] == LINHAS_ESPERADAS


def test_csv_deve_apresentar_resumo_e_detalhamento(repositorios):
    documento = RelatorioAcessoCSV(*repositorios).gerar()

    resumo, detalhamento = blocos_do_csv(documento.conteudo)
    assert documento.formato == "csv"
    assert resumo == [["total_acessos", "usuarios_distintos"], ["6", "3"]]
    assert detalhamento[0] == ["usuario_id", "login", "perfil", "quantidade"]
    assert detalhamento[1:] == LINHAS_ESPERADAS


def test_html_e_csv_devem_apresentar_os_mesmos_dados_na_mesma_ordem(repositorios):
    html = tabelas_do_html(RelatorioAcessoHTML(*repositorios).gerar().conteudo)
    resumo_csv, detalhamento_csv = blocos_do_csv(
        RelatorioAcessoCSV(*repositorios).gerar().conteudo
    )

    assert [linha[1] for linha in html["resumo"]] == resumo_csv[1]
    assert html["detalhamento"][1:] == detalhamento_csv[1:]


@pytest.mark.parametrize("formato", [RelatorioAcessoHTML, RelatorioAcessoCSV])
def test_sem_registros_deve_gerar_totais_zero_sem_linhas(formato):
    documento = formato(acessos_de(), UsuariosCadastrados([])).gerar()

    if formato is RelatorioAcessoHTML:
        tabelas = tabelas_do_html(documento.conteudo)
        valores = [linha[1] for linha in tabelas["resumo"]]
        linhas = tabelas["detalhamento"][1:]
    else:
        resumo, detalhamento = blocos_do_csv(documento.conteudo)
        valores = resumo[1]
        linhas = detalhamento[1:]

    assert valores == ["0", "0"]
    assert linhas == []


@pytest.mark.parametrize("formato", [RelatorioAcessoHTML, RelatorioAcessoCSV])
def test_documento_nao_deve_conter_senha_nem_email(formato, repositorios):
    conteudo = formato(*repositorios).gerar().conteudo

    assert "Senha@2026" not in conteudo
    assert "@example.com" not in conteudo


def test_html_deve_escapar_o_login():
    usuarios = UsuariosCadastrados([estudante(1, "<b>ana</b>&co")])

    conteudo = RelatorioAcessoHTML(acessos_de(1), usuarios).gerar().conteudo

    assert "<b>ana</b>" not in conteudo
    assert tabelas_do_html(conteudo)["detalhamento"][1][1] == "<b>ana</b>&co"


def test_csv_deve_preservar_login_com_virgula_e_aspas():
    usuarios = UsuariosCadastrados([estudante(1, 'ana, "a" silva')])

    conteudo = RelatorioAcessoCSV(acessos_de(1), usuarios).gerar().conteudo

    assert blocos_do_csv(conteudo)[1][1][1] == 'ana, "a" silva'


@pytest.mark.parametrize(
    "login",
    ["=cmd|'/c'!A", "+SUM(A:A)", "-SUM(A:A)", "@SUM(A:A)", "\tana", "\rana"],
)
def test_csv_deve_neutralizar_login_que_planilhas_tratariam_como_formula(login):
    usuarios = UsuariosCadastrados([estudante(1, login)])

    conteudo = RelatorioAcessoCSV(acessos_de(1), usuarios).gerar().conteudo

    assert blocos_do_csv(conteudo)[1][1][1] == "'" + login


def test_csv_nao_deve_alterar_login_comum_nem_os_numeros():
    usuarios = UsuariosCadastrados([estudante(1, "ana-maria")])

    conteudo = RelatorioAcessoCSV(acessos_de(1), usuarios).gerar().conteudo

    assert blocos_do_csv(conteudo)[1][1] == ["1", "ana-maria", "estudante", "1"]
