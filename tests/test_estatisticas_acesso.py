import pytest

from source.aplicacao.relatorios import (
    USUARIO_REMOVIDO,
    AcessosPorUsuario,
    Documento,
    EstatisticasAcesso,
    TemplateRelatorioAcesso,
)
from tests.apoio_relatorios import (
    UsuariosCadastrados,
    acessos_de,
    administrador,
    estudante,
)


class RelatorioDeTeste(TemplateRelatorioAcesso):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.passos = []

    def obter_estatisticas(self) -> EstatisticasAcesso:
        self.passos.append("obter_estatisticas")
        return super().obter_estatisticas()

    def formatar(self, estatisticas: EstatisticasAcesso) -> Documento:
        self.passos.append("formatar")
        return Documento(formato="teste", conteudo=repr(estatisticas))


def estatisticas(acessos, usuarios) -> EstatisticasAcesso:
    return RelatorioDeTeste(acessos, UsuariosCadastrados(usuarios)).obter_estatisticas()


def test_template_abstrato_nao_deve_ser_instanciado():
    with pytest.raises(TypeError):
        TemplateRelatorioAcesso(acessos_de(), UsuariosCadastrados([]))


def test_gerar_deve_obter_as_estatisticas_e_depois_formatar():
    relatorio = RelatorioDeTeste(acessos_de(1), UsuariosCadastrados([estudante(1, "ana")]))

    documento = relatorio.gerar()

    assert relatorio.passos == ["obter_estatisticas", "formatar"]
    assert documento.formato == "teste"
    assert "total_acessos=1" in documento.conteudo


def test_relatorio_com_acessos_deve_totalizar_e_detalhar_por_usuario():
    resultado = estatisticas(
        acessos_de(1, 2, 1, 2, 1),
        [estudante(1, "ana"), administrador(2, "bruno")],
    )

    assert resultado == EstatisticasAcesso(
        total_acessos=5,
        usuarios_distintos=2,
        detalhamento=(
            AcessosPorUsuario(1, "ana", "estudante", 3),
            AcessosPorUsuario(2, "bruno", "administrador", 2),
        ),
    )


def test_sem_registros_deve_ter_totais_zero_e_nenhuma_linha():
    resultado = estatisticas(acessos_de(), [estudante(1, "ana")])

    assert resultado == EstatisticasAcesso(
        total_acessos=0, usuarios_distintos=0, detalhamento=()
    )


def test_usuario_sem_acesso_nao_deve_aparecer_no_detalhamento():
    resultado = estatisticas(
        acessos_de(1), [estudante(1, "ana"), estudante(2, "bruno")]
    )

    assert [linha.login for linha in resultado.detalhamento] == ["ana"]


def test_detalhamento_deve_ordenar_por_quantidade_decrescente():
    resultado = estatisticas(
        acessos_de(1, 2, 2, 2, 3, 3),
        [estudante(1, "ana"), estudante(2, "bruno"), estudante(3, "carla")],
    )

    assert [(linha.login, linha.quantidade) for linha in resultado.detalhamento] == [
        ("bruno", 3),
        ("carla", 2),
        ("ana", 1),
    ]


def test_empate_na_quantidade_deve_ordenar_por_id_crescente():
    resultado = estatisticas(
        acessos_de(5, 2, 1, 5, 2, 1, 1),
        [estudante(1, "ana"), estudante(2, "bruno"), estudante(5, "carla")],
    )

    assert [(linha.usuario_id, linha.quantidade) for linha in resultado.detalhamento] == [
        (1, 3),
        (2, 2),
        (5, 2),
    ]


def test_acessos_de_usuario_removido_devem_continuar_contando():
    resultado = estatisticas(acessos_de(1, 1, 1, 7), [estudante(1, "ana")])

    assert resultado.total_acessos == 4
    assert resultado.usuarios_distintos == 2
    assert resultado.detalhamento == (
        AcessosPorUsuario(1, "ana", "estudante", 3),
        AcessosPorUsuario(7, USUARIO_REMOVIDO, USUARIO_REMOVIDO, 1),
    )


def test_deve_consultar_cada_usuario_distinto_uma_unica_vez():
    usuarios = UsuariosCadastrados([estudante(1, "ana"), estudante(2, "bruno")])

    RelatorioDeTeste(acessos_de(1, 2, 1, 1, 2), usuarios).obter_estatisticas()

    assert sorted(usuarios.consultas) == [1, 2]


def test_detalhamento_nao_deve_expor_senha_nem_email():
    resultado = estatisticas(acessos_de(1), [estudante(1, "ana")])

    campos = set(vars(resultado.detalhamento[0]))
    assert campos == {"usuario_id", "login", "perfil", "quantidade"}
