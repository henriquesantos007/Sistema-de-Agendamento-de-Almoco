from datetime import time
from typing import cast

import pytest

from source.aplicacao.restaurantes import (
    ControladorRestaurante,
    DadosRestauranteInvalidos,
    RestauranteNaoEncontrado,
    RestauranteVinculado,
    ValidadorRestaurante,
)
from source.dominio.restaurantes import DadosRestaurante, StatusRestaurante
from source.dominio.usuarios import GestorRestaurante
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
    RepositorioUsuariosMemoria,
)


def criar_dados_restaurante(
    nome: str = "Restaurante do CI",
    descricao: str = "Almocos no campus",
    localizacao: str = "Centro de Informatica",
    telefone: str = "83999990000",
    horario_limite_agendamento: time = time(10, 0),
) -> DadosRestaurante:
    return DadosRestaurante(
        nome=nome,
        descricao=descricao,
        localizacao=localizacao,
        telefone=telefone,
        horario_limite_agendamento=horario_limite_agendamento,
    )


@pytest.fixture
def repositorio():
    return RepositorioRestaurantesMemoria()


@pytest.fixture
def repositorio_usuarios():
    return RepositorioUsuariosMemoria()


@pytest.fixture
def controlador(repositorio, repositorio_usuarios):
    return ControladorRestaurante(
        repositorio,
        ValidadorRestaurante(),
        repositorio_usuarios,
    )


def test_deve_cadastrar_restaurante_normalizando_campos(controlador):
    restaurante = controlador.cadastrar(
        criar_dados_restaurante(
            nome=" Restaurante do CI ",
            localizacao=" Centro de Informatica ",
            telefone=" 83999990000 ",
        )
    )

    assert restaurante.id == 1
    assert restaurante.nome == "Restaurante do CI"
    assert restaurante.localizacao == "Centro de Informatica"
    assert restaurante.telefone == "83999990000"
    assert restaurante.status is StatusRestaurante.ATIVO


@pytest.mark.parametrize(
    ("campo", "mensagem"),
    [
        ("nome", "nome e obrigatorio"),
        ("localizacao", "localizacao e obrigatorio"),
        ("telefone", "telefone e obrigatorio"),
    ],
)
def test_deve_recusar_cadastro_com_campo_obrigatorio_vazio(
    controlador,
    campo,
    mensagem,
):
    valores = {
        "nome": "Restaurante",
        "localizacao": "Campus",
        "telefone": "83999990000",
        "horario_limite_agendamento": time(10, 0),
    }
    valores[campo] = "   "

    with pytest.raises(DadosRestauranteInvalidos) as erro:
        controlador.cadastrar(DadosRestaurante(**valores))

    assert mensagem in erro.value.erros
    assert controlador.listar_todos() == []


def test_deve_recusar_horario_limite_que_nao_seja_horario():
    dados = DadosRestaurante(
        nome="Restaurante",
        localizacao="Campus",
        telefone="83999990000",
        horario_limite_agendamento=cast(time, "10:00"),
    )
    validador = ValidadorRestaurante()

    assert validador.validar(dados) == [
        "horario limite de agendamento invalido"
    ]


def test_deve_buscar_e_listar_restaurantes(controlador):
    cadastrado = controlador.cadastrar(criar_dados_restaurante())

    assert controlador.buscar_por_id(cadastrado.id) is cadastrado
    assert controlador.listar_todos() == [cadastrado]


def test_deve_informar_quando_restaurante_nao_existe(controlador):
    with pytest.raises(RestauranteNaoEncontrado, match="restaurante nao encontrado"):
        controlador.buscar_por_id(999)


def test_deve_atualizar_dados_sem_mudar_identidade_e_status(controlador):
    cadastrado = controlador.cadastrar(criar_dados_restaurante())
    data_cadastro = cadastrado.data_cadastro

    atualizado = controlador.atualizar(
        cadastrado.id,
        criar_dados_restaurante(
            nome="Restaurante atualizado",
            localizacao="Novo local",
            telefone="83888880000",
            horario_limite_agendamento=time(9, 30),
        ),
    )

    assert atualizado is cadastrado
    assert atualizado.nome == "Restaurante atualizado"
    assert atualizado.localizacao == "Novo local"
    assert atualizado.telefone == "83888880000"
    assert atualizado.horario_limite_agendamento == time(9, 30)
    assert atualizado.id == cadastrado.id
    assert atualizado.data_cadastro == data_cadastro
    assert atualizado.status is StatusRestaurante.ATIVO


def test_deve_recusar_atualizacao_de_restaurante_inexistente(controlador):
    with pytest.raises(RestauranteNaoEncontrado):
        controlador.atualizar(999, criar_dados_restaurante())


def test_deve_preservar_dados_ao_recusar_atualizacao_invalida(controlador):
    restaurante = controlador.cadastrar(criar_dados_restaurante())

    with pytest.raises(DadosRestauranteInvalidos):
        controlador.atualizar(restaurante.id, criar_dados_restaurante(nome=" "))

    assert controlador.buscar_por_id(restaurante.id) is restaurante
    assert restaurante.nome == "Restaurante do CI"


def test_deve_remover_restaurante_e_retornar_resultado(controlador):
    restaurante = controlador.cadastrar(criar_dados_restaurante())

    assert controlador.remover(restaurante.id) is True
    assert controlador.listar_todos() == []
    assert controlador.remover(restaurante.id) is False


def test_deve_impedir_remocao_de_restaurante_com_gestor_vinculado(
    controlador,
    repositorio_usuarios,
):
    restaurante = controlador.cadastrar(criar_dados_restaurante())
    assert restaurante.id is not None
    repositorio_usuarios.adicionar(
        GestorRestaurante(
            nome="Gestor",
            login="gestor",
            email="gestor@example.com",
            senha="hash",
            telefone="83999990001",
            restaurante_id=restaurante.id,
        )
    )

    with pytest.raises(RestauranteVinculado):
        controlador.remover(restaurante.id)

    assert controlador.buscar_por_id(restaurante.id) is restaurante


def test_deve_remover_restaurante_se_gestor_estiver_vinculado_a_outro(
    controlador,
    repositorio_usuarios,
):
    restaurante = controlador.cadastrar(criar_dados_restaurante())
    assert restaurante.id is not None
    repositorio_usuarios.adicionar(
        GestorRestaurante(
            nome="Gestor",
            login="gestor",
            email="gestor@example.com",
            senha="hash",
            telefone="83999990001",
            restaurante_id=999,
        )
    )

    assert controlador.remover(restaurante.id) is True
