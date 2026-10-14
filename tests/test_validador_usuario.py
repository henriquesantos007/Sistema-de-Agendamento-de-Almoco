"""Testes unitarios das regras de validacao de credenciais do usuario.

Cobrem as regras de login e a politica de senha (padrao AWS IAM)
implementadas em source/dominio/usuarios/politica_credenciais.py.
"""

import pytest

from source.dominio.usuarios.excecoes import LoginInvalido, SenhaInvalida
from source.dominio.usuarios.politica_credenciais import (
    LOGIN_TAMANHO_MAXIMO,
    SENHA_TAMANHO_MAXIMO,
    SENHA_TAMANHO_MINIMO,
    SENHA_TIPOS_MINIMOS,
    validar_login,
    validar_senha,
)


# ---------------------------------------------------------------------------
# Regras de login
# ---------------------------------------------------------------------------


def test_deve_recusar_login_vazio():
    with pytest.raises(LoginInvalido):
        validar_login("")


def test_deve_recusar_login_apenas_com_espacos():
    with pytest.raises(LoginInvalido) as erro:
        validar_login("   ")

    assert "login e obrigatorio" in erro.value.motivos


def test_deve_recusar_login_acima_do_tamanho_maximo():
    with pytest.raises(LoginInvalido) as erro:
        validar_login("a" * (LOGIN_TAMANHO_MAXIMO + 1))

    assert any(
        "no maximo" in motivo for motivo in erro.value.motivos
    )


def test_deve_recusar_login_com_numeros():
    with pytest.raises(LoginInvalido) as erro:
        validar_login("usuario1")

    assert "login nao pode conter numeros" in erro.value.motivos


# ---------------------------------------------------------------------------
# Regras de senha (politica AWS IAM)
# ---------------------------------------------------------------------------


def test_deve_recusar_senha_menor_que_o_tamanho_minimo():
    senha = "Ab1!xyz"  # 7 caracteres, abaixo do minimo
    with pytest.raises(SenhaInvalida) as erro:
        validar_senha(senha)

    assert any("no minimo" in motivo for motivo in erro.value.motivos)


def test_deve_recusar_senha_maior_que_o_tamanho_maximo():
    senha = "Ab1!" + ("x" * (SENHA_TAMANHO_MAXIMO - 4 + 1))  # 129 caracteres
    with pytest.raises(SenhaInvalida) as erro:
        validar_senha(senha)

    assert any("no maximo" in motivo for motivo in erro.value.motivos)


def test_deve_recusar_senha_com_menos_de_tres_categorias():
    senha = "abcdefgh"  # apenas minusculas: 1 das 4 categorias
    with pytest.raises(SenhaInvalida) as erro:
        validar_senha(senha)

    assert any(
        f"ao menos {SENHA_TIPOS_MINIMOS} dos 4 tipos" in motivo
        for motivo in erro.value.motivos
    )


def test_deve_recusar_senha_identica_ao_login():
    senha = "Abcdef1!"
    with pytest.raises(SenhaInvalida) as erro:
        validar_senha(senha, login=senha)

    assert "senha nao pode ser identica ao login" in erro.value.motivos


# ---------------------------------------------------------------------------
# Cenarios de aceitacao (limites validos)
# ---------------------------------------------------------------------------


def test_deve_aceitar_login_valido():
    assert validar_login("victor") == "victor"


def test_deve_aceitar_login_com_tamanho_maximo():
    login = "a" * LOGIN_TAMANHO_MAXIMO
    assert validar_login(login) == login


def test_deve_aceitar_senha_com_tamanho_minimo():
    senha = "Ab1!" + ("x" * (SENHA_TAMANHO_MINIMO - 4))  # exatamente 8
    assert validar_senha(senha) is None


def test_deve_aceitar_senha_com_tamanho_maximo():
    senha = "Ab1!" + ("x" * (SENHA_TAMANHO_MAXIMO - 4))  # exatamente 128
    assert validar_senha(senha) is None


def test_deve_aceitar_senha_com_exatamente_tres_categorias():
    senha = "Abcdefg1"  # maiuscula + minusculas + numero: 3 categorias
    assert validar_senha(senha) is None


def test_deve_aceitar_senha_valida():
    senha = "SenhaForte1!"
    assert (
        validar_senha(senha, login="victor", email="victor@ci.ufpb.br") is None
    )
