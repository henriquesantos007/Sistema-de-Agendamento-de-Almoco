"""Testes de integracao da camada de aplicacao para o Controlador de Usuarios.

Garante o funcionamento do CRUD e a correta aplicacao das regras de validacao
durante a atualizacao e remocao de registros.
"""

import pytest

from source.aplicacao.usuarios.controlador_usuario import ControladorUsuario
from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.aplicacao.usuarios.validador_usuario import (
    ValidadorDadosObrigatorios,
    ValidadorEmail,
    ValidadorEstudante,
    ValidadorLogin,
    ValidadorPerfil,
    ValidadorUsuario,
)
from source.infraestrutura.persistencia.memoria.repositorio_usuarios_memoria import (
    RepositorioUsuariosMemoria,
)


@pytest.fixture
def controlador():
    """Fixture que prepara um controlador com repositorio em memoria e 2 usuarios cadastrados."""
    repositorio = RepositorioUsuariosMemoria()
    
    # Montamos o validador real para testar a logica do 'id_ignorado'
    validadores = [
        ValidadorDadosObrigatorios(),
        ValidadorPerfil(),
        ValidadorLogin(),
        ValidadorEmail(),
        ValidadorEstudante(),
    ]
    validador = ValidadorUsuario(validadores)
    
    ctrl = ControladorUsuario(repositorio, validador)

    # Populando o banco em memoria (IDs 1 e 2 gerados automaticamente)
    ctrl.cadastrar(DadosUsuario(
        perfil="estudante", nome="Ana Silva", login="anasilva",
        email="ana@example.com", senha="Senha123!",
        telefone="83999990001", matricula="2026001"
    ))
    ctrl.cadastrar(DadosUsuario(
        perfil="estudante", nome="Bruno Lima", login="brunolima",
        email="bruno@example.com", senha="Senha123!",
        telefone="83999990002", matricula="2026002"
    ))
    
    return ctrl


# ---------------------------------------------------------------------------
# Testes de Atualização
# ---------------------------------------------------------------------------

def test_deve_atualizar_usuario_com_sucesso_mantendo_dados_unicos(controlador):
    # Arrange: Preparando novos dados para a Ana (ID 1), mantendo email e matricula intactos
    novos_dados = DadosUsuario(
        perfil="estudante", nome="Ana Silva Modificada", login="anasilva",
        email="ana@example.com", senha="NovaSenha123!",
        telefone="83999990001", matricula="2026001"
    )

    # Act: Executando a atualizacao (isso vai testar se o id_ignorado funciona)
    usuario_atualizado = controlador.atualizar(1, novos_dados)

    # Assert: Verificando se atualizou sem levantar o falso positivo de duplicidade
    assert usuario_atualizado.nome == "Ana Silva Modificada"


def test_deve_retornar_erro_ao_atualizar_com_email_de_outro_usuario(controlador):
    # Arrange: Ana tenta roubar o e-mail que pertence ao Bruno (ID 2)
    dados_maliciosos = DadosUsuario(
        perfil="estudante", nome="Ana", login="anasilva",
        email="bruno@example.com", # Email do Bruno
        senha="Senha123!", telefone="83999990001", matricula="2026001"
    )

    # Act & Assert
    with pytest.raises(ValueError) as erro:
        controlador.atualizar(1, dados_maliciosos)

    assert "e-mail ja cadastrado" in str(erro.value)


def test_deve_retornar_erro_ao_atualizar_usuario_inexistente(controlador):
    dados = DadosUsuario(
        perfil="estudante", nome="Fantasma", login="fantasma",
        email="fantasma@example.com", senha="Senha123!",
        telefone="83999990009", matricula="2026999"
    )

    with pytest.raises(ValueError) as erro:
        controlador.atualizar(999, dados)

    assert "não encontrado" in str(erro.value).lower()


# ---------------------------------------------------------------------------
# Testes de Remoção
# ---------------------------------------------------------------------------

def test_deve_remover_usuario_com_sucesso(controlador):
    # Act: Removendo o Bruno (ID 2)
    controlador.remover(2)

    # Assert: O contador deve cair e a busca deve falhar
    assert controlador.contar() == 1
    with pytest.raises(ValueError) as erro:
        controlador.buscar_por_id(2)
    assert "não encontrado" in str(erro.value).lower()


def test_deve_retornar_erro_ao_remover_usuario_inexistente(controlador):
    # Act & Assert
    with pytest.raises(ValueError) as erro:
        controlador.remover(999)

    assert "não encontrado" in str(erro.value).lower()