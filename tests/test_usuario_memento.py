import pytest

from source.dominio.usuarios.usuario import Administrador, Estudante


def estudante(id_usuario: int) -> Estudante:
    return Estudante(
        nome="Ana",
        login="ana",
        email="ana@example.com",
        senha="hash",
        telefone="83999999999",
        matricula="2026001",
        id=id_usuario,
    )


def test_memento_restaura_snapshot_profundo_da_entidade():
    usuario = estudante(1)
    usuario.preferencias = {"notificacoes": ["email"]}
    memento = usuario.criar_memento()

    usuario.nome = "Alterado"
    usuario.preferencias["notificacoes"].append("sms")
    usuario.novo_atributo = True

    usuario.restaurar_memento(memento)

    assert usuario.nome == "Ana"
    assert usuario.preferencias == {"notificacoes": ["email"]}
    assert not hasattr(usuario, "novo_atributo")


def test_memento_nao_pode_ser_restaurado_em_classe_diferente():
    origem = estudante(1)
    destino = Administrador(
        nome="Admin",
        login="admin",
        email="admin@example.com",
        senha="hash",
        telefone="83988888888",
        id=1,
    )

    with pytest.raises(ValueError, match="não pertence"):
        destino.restaurar_memento(origem.criar_memento())


def test_memento_nao_pode_ser_restaurado_em_outro_id():
    origem = estudante(1)
    destino = estudante(2)

    with pytest.raises(ValueError, match="não pertence"):
        destino.restaurar_memento(origem.criar_memento())
