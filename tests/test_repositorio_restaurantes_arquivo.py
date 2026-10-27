import pickle
from datetime import time

import pytest

from source.dominio.restaurantes import DadosRestaurante, ErroPersistencia, Restaurante
from source.infraestrutura.persistencia.arquivo import (
    RepositorioRestaurantesArquivo,
)


def criar_restaurante(nome: str) -> Restaurante:
    return Restaurante(
        DadosRestaurante(
            nome=nome,
            descricao="Almocos no campus",
            localizacao="Centro de Informatica",
            telefone="83999990000",
            horario_limite_agendamento=time(10, 0),
        )
    )


def falhar_salvamento() -> None:
    raise ErroPersistencia("falha simulada")


def test_deve_persistir_criacao_atualizacao_e_remocao(tmp_path):
    caminho = tmp_path / "restaurantes.bin"
    repositorio = RepositorioRestaurantesArquivo(caminho)
    primeiro = repositorio.adicionar(criar_restaurante("Restaurante 1"))
    segundo = repositorio.adicionar(criar_restaurante("Restaurante 2"))
    segundo.atualizar_dados(
        DadosRestaurante(
            nome="Restaurante atualizado",
            descricao="Descricao",
            localizacao="Novo local",
            telefone="83888880000",
            horario_limite_agendamento=time(9, 30),
        )
    )
    repositorio.atualizar(segundo)
    assert repositorio.remover(primeiro.id) is True

    reaberto = RepositorioRestaurantesArquivo(caminho)

    assert reaberto.contar() == 1
    assert reaberto.buscar_por_id(segundo.id).nome == "Restaurante atualizado"
    assert reaberto.buscar_por_id(segundo.id).telefone == "83888880000"


def test_deve_reverter_cadastro_quando_gravacao_falhar(tmp_path):
    bloqueio = tmp_path / "arquivo"
    bloqueio.write_text("nao e um diretorio")
    caminho = bloqueio / "restaurantes.bin"
    repositorio = RepositorioRestaurantesArquivo(caminho)
    restaurante = criar_restaurante("Restaurante")

    with pytest.raises(ErroPersistencia):
        repositorio.adicionar(restaurante)

    assert repositorio.listar_todos() == []
    assert repositorio.contar() == 0
    assert restaurante.id is None


def test_deve_recarregar_estado_persistido_quando_atualizacao_falhar(
    tmp_path,
    monkeypatch,
):
    caminho = tmp_path / "restaurantes.bin"
    repositorio = RepositorioRestaurantesArquivo(caminho)
    restaurante = repositorio.adicionar(criar_restaurante("Nome original"))
    restaurante.atualizar_dados(
        DadosRestaurante(
            nome="Nome alterado",
            descricao="Almocos no campus",
            localizacao="Centro de Informatica",
            telefone="83999990000",
            horario_limite_agendamento=time(10, 0),
        )
    )
    monkeypatch.setattr(repositorio, "_salvar", falhar_salvamento)

    with pytest.raises(ErroPersistencia, match="falha simulada"):
        repositorio.atualizar(restaurante)

    assert repositorio.buscar_por_id(restaurante.id).nome == "Nome original"


def test_deve_recarregar_estado_persistido_quando_remocao_falhar(
    tmp_path,
    monkeypatch,
):
    caminho = tmp_path / "restaurantes.bin"
    repositorio = RepositorioRestaurantesArquivo(caminho)
    restaurante = repositorio.adicionar(criar_restaurante("Restaurante"))
    monkeypatch.setattr(repositorio, "_salvar", falhar_salvamento)

    with pytest.raises(ErroPersistencia, match="falha simulada"):
        repositorio.remover(restaurante.id)

    assert repositorio.buscar_por_id(restaurante.id).nome == "Restaurante"


@pytest.mark.parametrize("conteudo", [[], {"versao": 999}])
def test_deve_rejeitar_arquivo_com_formato_invalido(tmp_path, conteudo):
    caminho = tmp_path / "restaurantes.bin"
    caminho.write_bytes(pickle.dumps(conteudo))

    with pytest.raises(ErroPersistencia):
        RepositorioRestaurantesArquivo(caminho)
