from datetime import time

import pytest

from source.dominio.restaurantes import DadosRestaurante, Restaurante
from source.infraestrutura.persistencia.arquivo import (
    RepositorioRestaurantesArquivo,
    RepositorioUsuariosArquivo,
)
from source.infraestrutura.persistencia.fabrica_repositorios import (
    FabricaRepositorios,
    FabricaRepositoriosArquivo,
    FabricaRepositoriosMemoria,
)
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
    RepositorioUsuariosMemoria,
)


def test_fabrica_abstrata_nao_deve_ser_instanciada():
    with pytest.raises(TypeError):
        FabricaRepositorios()


def test_fabricas_concretas_devem_implementar_a_fabrica_abstrata():
    assert isinstance(FabricaRepositoriosMemoria(), FabricaRepositorios)
    assert isinstance(FabricaRepositoriosArquivo(), FabricaRepositorios)


def test_fabrica_de_memoria_deve_criar_repositorios_em_memoria():
    fabrica = FabricaRepositoriosMemoria()

    assert isinstance(
        fabrica.criar_repositorio_usuarios(), RepositorioUsuariosMemoria
    )
    assert isinstance(
        fabrica.criar_repositorio_restaurantes(), RepositorioRestaurantesMemoria
    )


def test_fabrica_de_memoria_deve_criar_um_repositorio_novo_a_cada_chamada():
    fabrica = FabricaRepositoriosMemoria()

    assert (
        fabrica.criar_repositorio_usuarios()
        is not fabrica.criar_repositorio_usuarios()
    )


def test_fabrica_de_arquivo_deve_criar_repositorios_nos_caminhos_informados(
    tmp_path,
):
    caminho_usuarios = tmp_path / "usuarios.bin"
    caminho_restaurantes = tmp_path / "restaurantes.bin"
    fabrica = FabricaRepositoriosArquivo(
        caminho_usuarios=caminho_usuarios,
        caminho_restaurantes=caminho_restaurantes,
    )

    usuarios = fabrica.criar_repositorio_usuarios()
    restaurantes = fabrica.criar_repositorio_restaurantes()
    restaurantes.adicionar(
        Restaurante(
            DadosRestaurante(
                nome="Restaurante",
                localizacao="Campus",
                telefone="83999990000",
                horario_limite_agendamento=time(10, 0),
            )
        )
    )

    assert isinstance(usuarios, RepositorioUsuariosArquivo)
    assert isinstance(restaurantes, RepositorioRestaurantesArquivo)
    assert caminho_restaurantes.exists()


def test_fabrica_de_arquivo_deve_usar_caminhos_padrao_quando_nao_informados(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    fabrica = FabricaRepositoriosArquivo()

    restaurantes = fabrica.criar_repositorio_restaurantes()
    restaurantes.adicionar(
        Restaurante(
            DadosRestaurante(
                nome="Restaurante",
                localizacao="Campus",
                telefone="83999990000",
                horario_limite_agendamento=time(10, 0),
            )
        )
    )

    assert (tmp_path / "dados" / "restaurantes.bin").exists()
