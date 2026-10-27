import argparse
from datetime import time

from source.aplicacao.fachada import FacadeSingletonController
from source.aplicacao.restaurantes import (
    DadosRestauranteInvalidos,
    RestauranteNaoEncontrado,
    RestauranteVinculado,
)
from source.aplicacao.usuarios import DadosUsuario, DadosUsuarioInvalidos
from source.dominio.restaurantes import DadosRestaurante
from source.dominio.restaurantes import ErroPersistencia as ErroPersistenciaRestaurantes
from source.dominio.usuarios import ErroPersistencia
from source.infraestrutura.persistencia.fabrica_repositorio import (
    ARMAZENAMENTOS,
    criar_repositorio_restaurantes,
    criar_repositorio_usuarios,
)

ERROS_DE_PERSISTENCIA = (ErroPersistencia, ErroPersistenciaRestaurantes)


def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cadastro de usuários e restaurantes")
    parser.add_argument(
        "--armazenamento",
        choices=ARMAZENAMENTOS,
        default="memoria",
        help="Mecanismo de persistência (padrão: memoria)",
    )
    parser.add_argument(
        "--caminho",
        default=None,
        help="Arquivo de usuários (padrão: dados/usuarios.bin)",
    )
    return parser.parse_args()


def tentar_cadastrar_usuario(fachada: FacadeSingletonController, dados: DadosUsuario) -> None:
    try:
        usuario = fachada.cadastrar_usuario(dados)
        print(f"Cadastrado: {usuario.perfil} '{usuario.login}' (id={usuario.id})")
    except DadosUsuarioInvalidos as erro:
        print(f"Cadastro de '{dados.login}' recusado:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")
    except ERROS_DE_PERSISTENCIA as erro:
        print(f"Falha de persistência ao cadastrar '{dados.login}': {erro}")


def tentar_cadastrar_restaurante(fachada: FacadeSingletonController, dados: DadosRestaurante):
    try:
        restaurante = fachada.cadastrar_restaurante(dados)
        print(f"Cadastrado: restaurante '{restaurante.nome}' (id={restaurante.id})")
        return restaurante
    except DadosRestauranteInvalidos as erro:
        print(f"Cadastro de restaurante '{dados.nome}' recusado:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")
    except ERROS_DE_PERSISTENCIA as erro:
        print(f"Falha de persistência ao cadastrar '{dados.nome}': {erro}")
    return None


def tentar_remover_restaurante(fachada: FacadeSingletonController, restaurante_id: int) -> None:
    try:
        removido = fachada.remover_restaurante(restaurante_id)
        print(f"Restaurante {restaurante_id} removido: {removido}")
    except (RestauranteNaoEncontrado, RestauranteVinculado) as erro:
        print(f"Remoção recusada: {erro}")
    except ERROS_DE_PERSISTENCIA as erro:
        print(f"Falha de persistência ao remover o restaurante: {erro}")


def executar_cenario_demonstracao(fachada: FacadeSingletonController) -> None:
    tentar_cadastrar_usuario(fachada, DadosUsuario(
        perfil="estudante",
        nome="Ana Silva",
        login="anasilva",
        email="ana@example.com",
        senha="Senha@2026",
        telefone="83999990000",
        matricula="2026001",
    ))

    tentar_cadastrar_usuario(fachada, DadosUsuario(
        perfil="estudante",
        nome="Bruno Lima",
        login="bruno123456789",
        email="bruno@example.com",
        senha="curta",
        telefone="83988880000",
        matricula="2026002",
    ))

    restaurante = tentar_cadastrar_restaurante(fachada, DadosRestaurante(
        nome="Restaurante do CI",
        descricao="Almoços no campus",
        localizacao="Centro de Informática",
        telefone="83977770000",
        horario_limite_agendamento=time(10, 0),
    ))

    if restaurante is not None:
        tentar_cadastrar_usuario(fachada, DadosUsuario(
            perfil="gestor_restaurante",
            nome="Carlos Souza",
            login="carlossouza",
            email="carlos@example.com",
            senha="Senha@2026",
            telefone="83966660000",
            restaurante_id=restaurante.id,
        ))
        tentar_remover_restaurante(fachada, restaurante.id)


def exibir_relatorio_final(fachada: FacadeSingletonController) -> None:
    try:
        usuarios = fachada.listar_usuarios()
        restaurantes = fachada.listar_restaurantes()
    except ERROS_DE_PERSISTENCIA as erro:
        print(f"Falha de persistência ao listar: {erro}")
        return

    print("\nUsuários armazenados:")
    for usuario in usuarios:
        print(f"  [{usuario.id}] {usuario.perfil} | {usuario.login} | {usuario.email}")

    print("\nRestaurantes armazenados:")
    for item in restaurantes:
        print(f"  [{item.id}] {item.nome} | {item.localizacao}")

    print("\n--- Resumo de Entidades ---")
    print(f"Usuários cadastrados: {fachada.contar_usuarios()}")
    print(f"Restaurantes cadastrados: {fachada.contar_restaurantes()}")
    print(f"Total de entidades cadastradas: {fachada.contar_total_entidades()}")


def main():
    argumentos = ler_argumentos()

    try:
        fachada = FacadeSingletonController.obter_instancia(
            criar_repositorio_usuarios(argumentos.armazenamento, argumentos.caminho),
            criar_repositorio_restaurantes(argumentos.armazenamento),
        )
    except ERROS_DE_PERSISTENCIA as erro:
        print(f"Não foi possível iniciar o armazenamento: {erro}")
        return

    print(f"Armazenamento: {argumentos.armazenamento}")
    
    mesma_fachada = FacadeSingletonController.obter_instancia() is fachada
    print(f"Mesma instância da fachada: {mesma_fachada}\n")

    executar_cenario_demonstracao(fachada)
    exibir_relatorio_final(fachada)


if __name__ == "__main__":
    main()