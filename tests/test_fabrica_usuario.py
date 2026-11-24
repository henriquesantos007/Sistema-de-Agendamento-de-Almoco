import pytest

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.aplicacao.usuarios.fabrica_usuario import FabricaUsuario
from source.dominio.usuarios import (
    Administrador,
    DadosBasicosUsuario,
    Estudante,
    GestorRestaurante,
    Perfil,
    normalizar_telefone,
)


def basicos() -> DadosBasicosUsuario:
    return DadosBasicosUsuario(
        nome="Ana", login="ana", email="ana@example.com", senha="hash", telefone="83999990000"
    )


def dados(perfil: str) -> DadosUsuario:
    return DadosUsuario(
        perfil=perfil,
        nome="Ana",
        login="ana",
        email="ana@example.com",
        senha="Senha@2026",
        telefone="83999990000",
        matricula="2026001",
        restaurante_id=3,
    )


@pytest.mark.parametrize(
    "perfil, classe",
    [
        (Perfil.ESTUDANTE, Estudante),
        (Perfil.GESTOR_RESTAURANTE, GestorRestaurante),
        (Perfil.ADMINISTRADOR, Administrador),
    ],
)
def test_fabrica_cria_usuario_do_perfil(perfil, classe):
    usuario = FabricaUsuario().criar(perfil, basicos(), dados(perfil.value))

    assert type(usuario) is classe
    assert usuario.perfil == perfil.value
    assert usuario.login == "ana"


def test_perfil_de_texto_ignora_caixa_e_espacos():
    assert Perfil.de_texto("  Estudante ") is Perfil.ESTUDANTE
    assert Perfil.de_texto("outro") is None
    assert Perfil.de_texto(None) is None


def test_normalizar_telefone_remove_nao_digitos():
    assert normalizar_telefone("(83) 99999-0000") == "83999990000"
