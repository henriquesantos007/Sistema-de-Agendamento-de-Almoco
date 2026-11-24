from unittest.mock import Mock

from source.aplicacao.comandos.comando_atualizar_usuario import (
    ComandoAtualizarUsuario,
)
from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.dominio.usuarios.usuario import Estudante


def test_comando_atualiza_e_restaura_o_snapshot_anterior():
    usuario = Estudante(
        nome="Ana",
        login="ana",
        email="ana@example.com",
        senha="hash",
        telefone="83999999999",
        matricula="2026001",
        id=1,
    )
    controlador = Mock()
    repositorio = Mock()
    repositorio.buscar_por_id.return_value = usuario
    repositorio.atualizar.return_value = usuario
    dados = DadosUsuario(
        perfil="estudante",
        nome="Ana Modificada",
        login="ana",
        email="ana.mod@example.com",
        senha="NovaSenha123!",
        telefone="83988888888",
        matricula="2026001",
    )
    controlador.atualizar.return_value = usuario
    comando = ComandoAtualizarUsuario(controlador, repositorio, 1, dados)

    assert comando.executar() is usuario
    controlador.atualizar.assert_called_once_with(1, dados)
    repositorio.buscar_por_id.assert_called_once_with(1)

    usuario.nome = "Ana Modificada"
    usuario.email = "ana.mod@example.com"
    usuario.matricula = "valor-mutado"

    assert comando.desfazer() is usuario

    assert usuario.nome == "Ana"
    assert usuario.email == "ana@example.com"
    assert usuario.matricula == "2026001"
    repositorio.atualizar.assert_called_once_with(usuario)
