from datetime import time

import pytest

from source.dominio.restaurantes import DadosRestaurante, Restaurante
from source.infraestrutura.persistencia.arquivo import (
    RepositorioRestaurantesArquivo,
)
from source.infraestrutura.persistencia.fabrica_repositorio import (
    criar_repositorio_restaurantes,
)
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
)


def test_deve_criar_repositorio_em_memoria_por_padrao():
    assert isinstance(
        criar_repositorio_restaurantes(),
        RepositorioRestaurantesMemoria,
    )


def test_deve_criar_repositorio_em_arquivo_com_caminho_especificado(tmp_path):
    caminho = tmp_path / "restaurantes.bin"

    repositorio = criar_repositorio_restaurantes("arquivo", caminho)
    repositorio.adicionar(
        Restaurante(
            DadosRestaurante(
                nome="Restaurante",
                localizacao="Campus",
                telefone="83999990000",
                horario_limite_agendamento=time(10, 0),
            )
        )
    )

    assert isinstance(repositorio, RepositorioRestaurantesArquivo)
    assert caminho.exists()


def test_deve_recusar_mecanismo_de_persistencia_desconhecido():
    with pytest.raises(ValueError, match="armazenamento invalido"):
        criar_repositorio_restaurantes("sqlite")
