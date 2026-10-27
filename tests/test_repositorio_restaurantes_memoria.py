from datetime import time
from typing import Optional

import pytest

from source.dominio.restaurantes import DadosRestaurante, Restaurante
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
)


def criar_restaurante(nome: str) -> Restaurante:
    return Restaurante(
        DadosRestaurante(
            nome=nome,
            localizacao="Centro de Informatica",
            telefone="83999990000",
            horario_limite_agendamento=time(10, 0),
        )
    )


def test_deve_adicionar_restaurantes_com_ids_sequenciais():
    repositorio = RepositorioRestaurantesMemoria()
    primeiro = criar_restaurante("Restaurante 1")
    segundo = criar_restaurante("Restaurante 2")

    assert repositorio.adicionar(primeiro) is primeiro
    assert repositorio.adicionar(segundo) is segundo
    assert primeiro.id == 1
    assert segundo.id == 2


def test_deve_contar_restaurantes_cadastrados():
    repositorio = RepositorioRestaurantesMemoria()
    repositorio.adicionar(criar_restaurante("Restaurante 1"))
    repositorio.adicionar(criar_restaurante("Restaurante 2"))

    assert repositorio.contar() == 2


def test_deve_impedir_cadastro_duplicado_da_mesma_instancia():
    repositorio = RepositorioRestaurantesMemoria()
    restaurante = criar_restaurante("Restaurante")
    repositorio.adicionar(restaurante)

    with pytest.raises(ValueError, match="ja cadastrado"):
        repositorio.adicionar(restaurante)

    assert repositorio.contar() == 1


def test_deve_buscar_por_id_ou_retornar_none_quando_nao_existir():
    repositorio = RepositorioRestaurantesMemoria()
    restaurante = repositorio.adicionar(criar_restaurante("Restaurante"))

    assert repositorio.buscar_por_id(restaurante.id) is restaurante
    assert repositorio.buscar_por_id(999) is None


def test_deve_listar_todos_sem_expor_a_lista_interna():
    repositorio = RepositorioRestaurantesMemoria()
    restaurante = repositorio.adicionar(criar_restaurante("Restaurante"))

    restaurantes = repositorio.listar_todos()
    restaurantes.clear()

    assert repositorio.listar_todos() == [restaurante]


def test_deve_atualizar_restaurante_existente():
    repositorio = RepositorioRestaurantesMemoria()
    cadastrado = repositorio.adicionar(criar_restaurante("Nome antigo"))
    atualizado = criar_restaurante("Nome novo")
    atualizado.id = cadastrado.id
    atualizado.atualizar_dados(
        DadosRestaurante(
            nome="Nome novo",
            descricao="Descricao",
            localizacao="Nova localizacao",
            telefone="83888880000",
            horario_limite_agendamento=time(9, 30),
        )
    )

    assert repositorio.atualizar(atualizado) is atualizado
    assert repositorio.buscar_por_id(cadastrado.id) is atualizado
    assert atualizado.nome == "Nome novo"


@pytest.mark.parametrize(
    "restaurante_id",
    [None, 999],
)
def test_deve_recusar_atualizacao_de_restaurante_inexistente(
    restaurante_id: Optional[int],
):
    repositorio = RepositorioRestaurantesMemoria()
    restaurante = criar_restaurante("Nao cadastrado")
    if restaurante_id is not None:
        restaurante.id = restaurante_id

    with pytest.raises(ValueError, match="restaurante"):
        repositorio.atualizar(restaurante)


def test_deve_remover_restaurante_existente_e_atualizar_contagem():
    repositorio = RepositorioRestaurantesMemoria()
    restaurante = repositorio.adicionar(criar_restaurante("Restaurante"))

    assert repositorio.remover(restaurante.id) is True
    assert repositorio.buscar_por_id(restaurante.id) is None
    assert repositorio.contar() == 0


def test_deve_retornar_false_ao_remover_restaurante_inexistente():
    repositorio = RepositorioRestaurantesMemoria()

    assert repositorio.remover(999) is False
    assert repositorio.contar() == 0


def test_deve_manter_sequencia_de_ids_apos_remocao():
    repositorio = RepositorioRestaurantesMemoria()
    primeiro = repositorio.adicionar(criar_restaurante("Restaurante 1"))
    repositorio.adicionar(criar_restaurante("Restaurante 2"))

    repositorio.remover(primeiro.id)
    terceiro = repositorio.adicionar(criar_restaurante("Restaurante 3"))

    assert terceiro.id == 3
    assert repositorio.contar() == 2
