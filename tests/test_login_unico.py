"""Testes da regra de login unico no cadastro de usuarios.

Cobrem a consulta RepositorioUsuariosMemoria.existe_login, a checagem feita
pelo ValidadorLogin e o comportamento do ControladorUsuario ao receber um
login repetido.
"""

import pytest

from source.aplicacao.usuarios import (
    ControladorUsuario,
    DadosUsuario,
    DadosUsuarioInvalidos,
)
from source.aplicacao.usuarios.validador_usuario import (
    ValidadorLogin,
    ValidadorUsuario,
)
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria

MENSAGEM_LOGIN_REPETIDO = "login ja cadastrado"


def criar_dados(login: str, email: str = "victor@ci.ufpb.br") -> DadosUsuario:
    return DadosUsuario(
        perfil="administrador",
        nome="Victor",
        login=login,
        email=email,
        senha="Almoco#2026",
        telefone="83999990000",
    )


@pytest.fixture
def repositorio():
    return RepositorioUsuariosMemoria()


@pytest.fixture
def controlador(repositorio):
    return ControladorUsuario(repositorio, ValidadorUsuario([ValidadorLogin()]))


def test_deve_informar_que_login_existe_apos_cadastro(controlador, repositorio):
    controlador.cadastrar(criar_dados("victor"))

    assert repositorio.existe_login("victor") is True


def test_deve_informar_que_login_nao_existe_em_repositorio_vazio(repositorio):
    assert repositorio.existe_login("victor") is False


def test_deve_recusar_login_ja_cadastrado(controlador):
    controlador.cadastrar(criar_dados("victor"))

    with pytest.raises(DadosUsuarioInvalidos) as erro:
        controlador.cadastrar(criar_dados("victor", email="outro@ci.ufpb.br"))

    assert MENSAGEM_LOGIN_REPETIDO in erro.value.erros


def test_deve_recusar_login_repetido_com_maiusculas_e_espacos(controlador):
    controlador.cadastrar(criar_dados("victor"))

    with pytest.raises(DadosUsuarioInvalidos) as erro:
        controlador.cadastrar(criar_dados(" Victor ", email="outro@ci.ufpb.br"))

    assert MENSAGEM_LOGIN_REPETIDO in erro.value.erros


def test_deve_manter_apenas_um_usuario_apos_login_repetido(controlador):
    controlador.cadastrar(criar_dados("victor"))

    with pytest.raises(DadosUsuarioInvalidos):
        controlador.cadastrar(criar_dados("victor", email="outro@ci.ufpb.br"))

    assert len(controlador.listar_todos()) == 1


def test_deve_aceitar_login_ainda_nao_cadastrado(controlador):
    controlador.cadastrar(criar_dados("victor"))

    usuario = controlador.cadastrar(criar_dados("ana", email="ana@ci.ufpb.br"))

    assert usuario.id == 2
