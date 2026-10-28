import copy
import threading
from datetime import time

import pytest

from source.aplicacao.fachada import FacadeSingletonController
from source.aplicacao.restaurantes import (
    DadosRestauranteInvalidos,
    RestauranteNaoEncontrado,
    RestauranteVinculado,
)
from source.aplicacao.usuarios import DadosUsuario, DadosUsuarioInvalidos
from source.dominio.restaurantes import DadosRestaurante
from source.infraestrutura.persistencia.arquivo import (
    RepositorioRestaurantesArquivo,
    RepositorioUsuariosArquivo,
)
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
    RepositorioUsuariosMemoria,
)


def dados_restaurante(nome="Restaurante do CI"):
    return DadosRestaurante(
        nome=nome,
        descricao="Almocos no campus",
        localizacao="Centro de Informatica",
        telefone="83999990000",
        horario_limite_agendamento=time(10, 0),
    )


def dados_estudante(login="anasilva", email="ana@example.com", matricula="2026001",
                    telefone="83999990001"):
    return DadosUsuario(
        perfil="estudante",
        nome="Ana Silva",
        login=login,
        email=email,
        senha="Senha@2026",
        telefone=telefone,
        matricula=matricula,
    )


def dados_gestor(restaurante_id, login="carlossouza", email="carlos@example.com",
                 telefone="83999990002"):
    return DadosUsuario(
        perfil="gestor_restaurante",
        nome="Carlos Souza",
        login=login,
        email=email,
        senha="Senha@2026",
        telefone=telefone,
        restaurante_id=restaurante_id,
    )


@pytest.fixture(autouse=True)
def fachada_limpa():
    FacadeSingletonController.reiniciar()
    yield
    FacadeSingletonController.reiniciar()


@pytest.fixture
def repositorios():
    return RepositorioUsuariosMemoria(), RepositorioRestaurantesMemoria()


@pytest.fixture
def fachada(repositorios):
    return FacadeSingletonController.obter_instancia(*repositorios)


# ---- Singleton ----

def test_obter_instancia_deve_devolver_sempre_a_mesma_fachada(repositorios):
    primeira = FacadeSingletonController.obter_instancia(*repositorios)

    assert FacadeSingletonController.obter_instancia() is primeira
    assert FacadeSingletonController.obter_instancia(*repositorios) is primeira


def test_construtor_direto_deve_ser_recusado():
    with pytest.raises(TypeError):
        FacadeSingletonController()


def test_copia_da_fachada_deve_ser_a_propria_instancia(fachada):
    assert copy.copy(fachada) is fachada
    assert copy.deepcopy(fachada) is fachada


def test_primeira_chamada_sem_repositorios_deve_falhar():
    with pytest.raises(ValueError):
        FacadeSingletonController.obter_instancia()


def test_primeira_chamada_com_repositorio_faltando_deve_falhar(repositorios):
    with pytest.raises(ValueError):
        FacadeSingletonController.obter_instancia(repositorios[0], None)

    assert FacadeSingletonController._instancia is None


def test_repositorios_diferentes_depois_da_criacao_devem_ser_recusados(fachada):
    with pytest.raises(ValueError):
        FacadeSingletonController.obter_instancia(
            RepositorioUsuariosMemoria(), RepositorioRestaurantesMemoria()
        )


def test_reiniciar_deve_permitir_nova_configuracao(fachada):
    FacadeSingletonController.reiniciar()

    nova = FacadeSingletonController.obter_instancia(
        RepositorioUsuariosMemoria(), RepositorioRestaurantesMemoria()
    )

    assert nova is not fachada


def test_threads_concorrentes_devem_receber_a_mesma_instancia(repositorios):
    instancias = []
    barreira = threading.Barrier(8)

    def pedir():
        barreira.wait()
        instancias.append(FacadeSingletonController.obter_instancia(*repositorios))

    threads = [threading.Thread(target=pedir) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(instancias) == 8
    assert len({id(instancia) for instancia in instancias}) == 1


def test_reiniciar_concorrente_nao_deve_quebrar_obter_instancia(fachada, monkeypatch):
    validar_original = FacadeSingletonController._validar_repositorios_inalterados

    def validar_apos_reiniciar(self, *repositorios):
        FacadeSingletonController.reiniciar()
        validar_original(self, *repositorios)

    monkeypatch.setattr(
        FacadeSingletonController,
        "_validar_repositorios_inalterados",
        validar_apos_reiniciar,
    )

    assert FacadeSingletonController.obter_instancia() is fachada


# ---- Facade: delegacao aos controladores ----

def test_deve_cadastrar_e_listar_usuarios(fachada):
    usuario = fachada.cadastrar_usuario(dados_estudante())

    assert usuario.id == 1
    assert fachada.listar_usuarios() == [usuario]


def test_cadastro_de_usuario_invalido_deve_levantar_erro_de_validacao(fachada):
    with pytest.raises(DadosUsuarioInvalidos):
        fachada.cadastrar_usuario(dados_estudante(login="ana1"))

    assert fachada.contar_usuarios() == 0


def test_deve_executar_crud_de_restaurante(fachada):
    restaurante = fachada.cadastrar_restaurante(dados_restaurante())
    assert fachada.buscar_restaurante(restaurante.id) is restaurante
    assert fachada.listar_restaurantes() == [restaurante]

    fachada.atualizar_restaurante(restaurante.id, dados_restaurante("Novo Nome"))
    assert fachada.buscar_restaurante(restaurante.id).nome == "Novo Nome"

    assert fachada.remover_restaurante(restaurante.id) is True
    assert fachada.listar_restaurantes() == []
    with pytest.raises(RestauranteNaoEncontrado):
        fachada.buscar_restaurante(restaurante.id)


def test_restaurante_invalido_deve_levantar_erro_de_validacao(fachada):
    with pytest.raises(DadosRestauranteInvalidos):
        fachada.cadastrar_restaurante(dados_restaurante(nome="  "))


def test_gestor_deve_exigir_restaurante_cadastrado_pela_mesma_fachada(fachada):
    with pytest.raises(DadosUsuarioInvalidos):
        fachada.cadastrar_usuario(dados_gestor(restaurante_id=99))

    restaurante = fachada.cadastrar_restaurante(dados_restaurante())
    gestor = fachada.cadastrar_usuario(dados_gestor(restaurante.id))

    assert gestor.restaurante_id == restaurante.id


def test_nao_deve_remover_restaurante_com_gestor_vinculado(fachada):
    restaurante = fachada.cadastrar_restaurante(dados_restaurante())
    fachada.cadastrar_usuario(dados_gestor(restaurante.id))

    with pytest.raises(RestauranteVinculado):
        fachada.remover_restaurante(restaurante.id)

    assert fachada.contar_restaurantes() == 1


# ---- Facade: contagem de entidades ----

def test_sistema_vazio_deve_ter_zero_entidades(fachada):
    assert fachada.contar_total_entidades() == 0
    assert fachada.obter_contagem_por_entidade() == {
        FacadeSingletonController.CHAVE_USUARIOS: 0, 
        FacadeSingletonController.CHAVE_RESTAURANTES: 0
    }


def test_deve_contar_entidades_de_todos_os_tipos(fachada):
    restaurante = fachada.cadastrar_restaurante(dados_restaurante())
    fachada.cadastrar_usuario(dados_estudante())
    fachada.cadastrar_usuario(dados_gestor(restaurante.id))

    assert fachada.contar_usuarios() == 2
    assert fachada.contar_restaurantes() == 1
    assert fachada.contar_total_entidades() == 3


def test_contagem_deve_diminuir_ao_remover_e_ignorar_cadastros_recusados(fachada):
    restaurante = fachada.cadastrar_restaurante(dados_restaurante())
    with pytest.raises(DadosUsuarioInvalidos):
        fachada.cadastrar_usuario(dados_estudante(login="ana1"))
    assert fachada.contar_total_entidades() == 1

    fachada.remover_restaurante(restaurante.id)

    assert fachada.contar_total_entidades() == 0


def test_contagem_deve_refletir_dados_persistidos_em_arquivo(tmp_path):
    def abrir():
        FacadeSingletonController.reiniciar()
        return FacadeSingletonController.obter_instancia(
            RepositorioUsuariosArquivo(tmp_path / "usuarios.bin"),
            RepositorioRestaurantesArquivo(tmp_path / "restaurantes.bin"),
        )

    primeira = abrir()
    restaurante = primeira.cadastrar_restaurante(dados_restaurante())
    primeira.cadastrar_usuario(dados_gestor(restaurante.id))
    assert primeira.contar_total_entidades() == 2

    segunda = abrir()

    assert segunda is not primeira
    assert segunda.contar_total_entidades() == 2
    assert segunda.obter_contagem_por_entidade() == {
        FacadeSingletonController.CHAVE_USUARIOS: 1, 
        FacadeSingletonController.CHAVE_RESTAURANTES: 1
    }