from datetime import time

import pytest

from source.aplicacao.usuarios import (
    ControladorUsuario,
    DadosUsuario,
    DadosUsuarioInvalidos,
    ValidadorGestorRestaurante,
)
from source.aplicacao.usuarios.validador_usuario import ValidadorUsuario
from source.dominio.restaurantes import DadosRestaurante, Restaurante
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
    RepositorioUsuariosMemoria,
)


def criar_dados_usuario(restaurante_id: int) -> DadosUsuario:
    return DadosUsuario(
        perfil="gestor_restaurante",
        nome="Gestor do CI",
        login="gestor",
        email="gestor@example.com",
        senha="SenhaForte1!",
        telefone="83999990000",
        restaurante_id=restaurante_id,
    )


def criar_controlador(repositorio_restaurantes):
    repositorio_usuarios = RepositorioUsuariosMemoria()
    validador = ValidadorUsuario(
        [ValidadorGestorRestaurante(repositorio_restaurantes)]
    )
    return ControladorUsuario(repositorio_usuarios, validador)


def test_deve_cadastrar_gestor_quando_restaurante_existe():
    repositorio_restaurantes = RepositorioRestaurantesMemoria()
    restaurante = repositorio_restaurantes.adicionar(
        Restaurante(
            DadosRestaurante(
                nome="Restaurante",
                localizacao="Campus",
                telefone="83999990000",
                horario_limite_agendamento=time(10, 0),
            )
        )
    )
    assert restaurante.id is not None
    controlador = criar_controlador(repositorio_restaurantes)

    gestor = controlador.cadastrar(criar_dados_usuario(restaurante.id))

    assert gestor.restaurante_id == restaurante.id


def test_deve_recusar_gestor_quando_restaurante_nao_existe():
    controlador = criar_controlador(RepositorioRestaurantesMemoria())

    with pytest.raises(DadosUsuarioInvalidos) as erro:
        controlador.cadastrar(criar_dados_usuario(999))

    assert "restaurante nao encontrado" in erro.value.erros
    assert controlador.listar_todos() == []


def test_deve_continuar_exigindo_restaurante_para_gestor():
    repositorio_restaurantes = RepositorioRestaurantesMemoria()
    controlador = criar_controlador(repositorio_restaurantes)
    dados = criar_dados_usuario(1)
    dados_sem_restaurante = DadosUsuario(
        perfil=dados.perfil,
        nome=dados.nome,
        login=dados.login,
        email=dados.email,
        senha=dados.senha,
        telefone=dados.telefone,
    )

    with pytest.raises(DadosUsuarioInvalidos) as erro:
        controlador.cadastrar(dados_sem_restaurante)

    assert "restaurante e obrigatorio para gestor" in erro.value.erros
