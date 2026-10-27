from datetime import datetime, time

from source.dominio.restaurantes import (
    DadosRestaurante,
    Restaurante,
    StatusRestaurante,
)


def criar_dados_restaurante(
    nome: str,
) -> DadosRestaurante:
    return DadosRestaurante(
        nome=nome,
        descricao="Almocos no campus",
        localizacao="Centro de Informatica",
        telefone="83999990000",
        horario_limite_agendamento=time(10, 0),
    )


def test_deve_criar_restaurante_com_identificacao_e_status_padrao():
    restaurante = Restaurante(
        criar_dados_restaurante(
            nome="Restaurante do CI",
            descricao="Almocos no campus",
        )
    )

    assert restaurante.id is None
    assert restaurante.nome == "Restaurante do CI"
    assert restaurante.descricao == "Almocos no campus"
    assert restaurante.localizacao == "Centro de Informatica"
    assert restaurante.telefone == "83999990000"
    assert restaurante.horario_limite_agendamento == time(10, 0)
    assert restaurante.status is StatusRestaurante.ATIVO
    assert isinstance(restaurante.data_cadastro, datetime)


def test_deve_atualizar_dados_sem_alterar_id_data_ou_status():
    data_cadastro = datetime(2026, 1, 1, 12, 0)
    restaurante = Restaurante(criar_dados_restaurante("Restaurante antigo"))
    restaurante.id = 7
    restaurante.data_cadastro = data_cadastro
    restaurante.status = StatusRestaurante.INATIVO

    restaurante.atualizar_dados(
        DadosRestaurante(
            nome="Restaurante novo",
            descricao="Descricao nova",
            localizacao="Local novo",
            telefone="83888880000",
            horario_limite_agendamento=time(9, 30),
        )
    )

    assert restaurante.nome == "Restaurante novo"
    assert restaurante.descricao == "Descricao nova"
    assert restaurante.localizacao == "Local novo"
    assert restaurante.telefone == "83888880000"
    assert restaurante.horario_limite_agendamento == time(9, 30)
    assert restaurante.id == 7
    assert restaurante.data_cadastro == data_cadastro
    assert restaurante.status is StatusRestaurante.INATIVO
