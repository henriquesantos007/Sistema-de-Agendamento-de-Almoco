import argparse
import re
from datetime import time

from source.aplicacao.fachada import FacadeSingletonController
from source.aplicacao.relatorios import FormatoRelatorioInvalido
from source.aplicacao.restaurantes import (
    DadosRestauranteInvalidos,
    RestauranteVinculado,
)
from source.aplicacao.usuarios import DadosUsuario, DadosUsuarioInvalidos
from source.dominio.excecoes import ErroPersistenciaBase
from source.dominio.restaurantes import DadosRestaurante
from source.infraestrutura.logs import criar_adaptador_logging
from source.infraestrutura.persistencia.fabrica_repositorios import (
    FabricaRepositorios,
    FabricaRepositoriosArquivo,
    FabricaRepositoriosMemoria,
)

ARMAZENAMENTO_MEMORIA = "memoria"
ARMAZENAMENTO_ARQUIVO = "arquivo"
ARMAZENAMENTOS = (ARMAZENAMENTO_MEMORIA, ARMAZENAMENTO_ARQUIVO)


def ler_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cadastro de usuários e restaurantes")
    parser.add_argument(
        "--armazenamento",
        choices=ARMAZENAMENTOS,
        default=ARMAZENAMENTO_MEMORIA,
        help="Mecanismo de persistência (padrão: memoria)",
    )
    parser.add_argument(
        "--caminho",
        default=None,
        help="Arquivo de usuários (padrão: dados/usuarios.bin)",
    )
    parser.add_argument(
        "--caminho-restaurantes",
        default=None,
        help="Arquivo de restaurantes (padrão: dados/restaurantes.bin)",
    )
    parser.add_argument(
        "--caminho-acessos",
        default=None,
        help="Arquivo de registros de acesso (padrão: dados/acessos.jsonl)",
    )
    return parser.parse_args()


def escolher_fabrica(argumentos: argparse.Namespace) -> FabricaRepositorios:
    if argumentos.armazenamento == ARMAZENAMENTO_ARQUIVO:
        return FabricaRepositoriosArquivo(
            caminho_usuarios=argumentos.caminho,
            caminho_restaurantes=argumentos.caminho_restaurantes,
            caminho_acessos=argumentos.caminho_acessos,
        )
    return FabricaRepositoriosMemoria()


# Funções Auxiliares de Formatação

def formatar_telefone(telefone: str) -> str:
    """Aplica a máscara (XX) XXXXX-XXXX em strings contendo números."""
    if not telefone:
        return "Não informado"
    numeros = re.sub(r"\D", "", telefone)
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return telefone


def formatar_dados_usuario(dados: DadosUsuario) -> str:
    linhas = [
        f"perfil: {dados.perfil}",
        f"nome: {dados.nome}",
        f"login: {dados.login}",
        f"email: {dados.email}",
        f"senha: {dados.senha}",
        f"telefone: {formatar_telefone(dados.telefone)}"
    ]
    if dados.perfil == "estudante":
        linhas.append(f"matrícula: {dados.matricula}")
    elif dados.perfil == "gestor_restaurante":
        linhas.append(f"id_do restaurante: {dados.restaurante_id}")
    return "\n".join(linhas)


def formatar_dados_restaurante(dados: DadosRestaurante) -> str:
    limite = dados.horario_limite_agendamento.strftime('%H:%M') + "hrs" if dados.horario_limite_agendamento else "Não informado"
    linhas = [
        f"nome: {dados.nome}",
        f"descrição: {dados.descricao}",
        f"localizacao: {dados.localizacao}",
        f"telefone: {formatar_telefone(dados.telefone)}",
        f"horario_limite_agendamento: {limite}"
    ]
    return "\n".join(linhas)


def imprimir_detalhes_restaurante(restaurante) -> None:
    """Imprime as propriedades de uma entidade Restaurante de forma estruturada."""
    print(f"\nnome: {restaurante.nome}")
    print(f"descrição: {restaurante.descricao}")
    print(f"localizacao: {restaurante.localizacao}")
    print(f"telefone: {formatar_telefone(restaurante.telefone)}")
    
    if restaurante.horario_limite_agendamento:
        print(f"horario_limite_agendamento: {restaurante.horario_limite_agendamento.strftime('%H:%M')}hrs\n")
    else:
        print("horario_limite_agendamento: Não informado\n")


def imprimir_detalhes_usuario(usuario, titulo="Antes:") -> None:
    """Imprime as propriedades de uma entidade Usuario de forma estruturada."""
    print(titulo)
    print(f"- perfil: {usuario.perfil}")
    print(f"- nome: {usuario.nome}")
    print(f"- login: {usuario.login}")
    print(f"- email: {usuario.email}")
    print("- senha: (oculta)")
    print(f"- telefone: {formatar_telefone(usuario.telefone)}")
    
    if usuario.perfil == "estudante":
        print(f"- matrícula: {getattr(usuario, 'matricula', 'Não informado')}")
    elif usuario.perfil == "gestor_restaurante":
        print(f"- id_do restaurante: {getattr(usuario, 'restaurante_id', 'Não informado')}")


# Funções de Ação/Tentativa (Com formatação em trilha acoplada)

def tentar_cadastrar_usuario(fachada: FacadeSingletonController, dados: DadosUsuario, titulo: str) -> None:
    print(f"{titulo}\n-----------------------------------------")
    print(f"\n{formatar_dados_usuario(dados)}\n")
    try:
        usuario = fachada.cadastrar_usuario(dados)
        print(f"Cadastrado: {usuario.perfil} '{usuario.login}' (id={usuario.id})")
    except DadosUsuarioInvalidos as erro:
        print(f"Cadastro de '{dados.login}' recusado:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")
    except ErroPersistenciaBase as erro:
        print(f"Falha de persistência ao cadastrar '{dados.login}': {erro}")
    print("-----------------------------------------\n")


def tentar_cadastrar_restaurante(fachada: FacadeSingletonController, dados: DadosRestaurante, titulo: str):
    print(f"{titulo}\n-----------------------------------------")
    print(f"\n{formatar_dados_restaurante(dados)}\n")
    try:
        restaurante = fachada.cadastrar_restaurante(dados)
        print(f"Cadastrado: restaurante '{restaurante.nome}' (id={restaurante.id})")
        print("-----------------------------------------\n")
        return restaurante
    except DadosRestauranteInvalidos as erro:
        print(f"Cadastro de restaurante '{dados.nome}' recusado:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")
    except ErroPersistenciaBase as erro:
        print(f"Falha de persistência ao cadastrar '{dados.nome}': {erro}")
    print("-----------------------------------------\n")
    return None


def tentar_remover_restaurante(fachada: FacadeSingletonController, restaurante_id: int) -> None:
    print("Restaurante:\n-----------------------------------------")
    # Busca os dados atuais para imprimir antes de deletar
    try:
        rest_atual = fachada.buscar_restaurante(restaurante_id)
        imprimir_detalhes_restaurante(rest_atual)
    except ValueError:
        pass # Se não existir, ignora a impressão detalhada e deixa o erro ser tratado abaixo

    try:
        if fachada.remover_restaurante(restaurante_id):
            print(f"Restaurante {restaurante_id} removido.")
        else:
            print(f"Remoção recusada: restaurante {restaurante_id} não encontrado.")
    except RestauranteVinculado as erro:
        print(f"Remoção recusada: {erro}")
    except ErroPersistenciaBase as erro:
        print(f"Falha de persistência ao remover o restaurante: {erro}")
    print("-----------------------------------------\n")


def tentar_atualizar_usuario(fachada: FacadeSingletonController, usuario_id: int, dados: DadosUsuario, titulo: str) -> None:
    print(f"{titulo}\n-----------------------------------------")
    # Resgata os dados antes da atualização
    try:
        usr_antes = fachada.buscar_usuario(usuario_id)
        imprimir_detalhes_usuario(usr_antes, titulo="Antes:")
    except ValueError:
        print(f"Usuário {usuario_id} não encontrado.")
        print("-----------------------------------------\n")
        return

    try:
        usr_depois = fachada.atualizar_usuario(usuario_id, dados)
        print("\nDepois:")
        print(f"- nome: {usr_depois.nome}")
        print(f"- email: {usr_depois.email}")
    except DadosUsuarioInvalidos as erro:
        print("\nAtualização recusada:")
        for mensagem in erro.erros:
            print(f"  - {mensagem}")
    except ValueError as erro:
        print(f"\nAtualização recusada: {erro}")
    except ErroPersistenciaBase as erro:
        print(f"\nFalha de persistência: {erro}")
    print("-----------------------------------------\n")


def tentar_remover_usuario(fachada: FacadeSingletonController, usuario_id: int, titulo: str) -> None:
    print(f"{titulo}\n-----------------------------------------")
    try:
        fachada.remover_usuario(usuario_id)
        print(f"\nUsuário {usuario_id} removido com sucesso.")
    except ValueError as erro:
        print(f"\nRemoção recusada: {erro}")
    except ErroPersistenciaBase as erro:
        print(f"\nFalha de persistência: {erro}")
    print("-----------------------------------------\n")


def tentar_gerar_relatorio_acessos(fachada: FacadeSingletonController, formato: str) -> None:
    try:
        documento = fachada.gerar_relatorio_acessos(formato)
        print(f"Relatório de acessos em {documento.formato.upper()}:")
        print(documento.conteudo)
    except FormatoRelatorioInvalido as erro:
        print(f"Relatório de acessos em '{formato}' recusado: {erro}")
    except ErroPersistenciaBase as erro:
        print(f"Falha de persistência ao gerar o relatório de acessos: {erro}")


# CENÁRIO DE DEMONSTRAÇÃO

def executar_cenario_demonstracao(fachada: FacadeSingletonController) -> None:
    print("=========================================\n1 - CADASTROS DE USUÁRIOS\n=========================================")
    
    tentar_cadastrar_usuario(fachada, DadosUsuario(
        perfil="estudante", nome="Ana Silva", login="anasilva",
        email="ana@example.com", senha="Senha@2026",
        telefone="83999990000", matricula="2026001"
    ), "\nUsuário 01:")

    tentar_cadastrar_usuario(fachada, DadosUsuario(
        perfil="estudante", nome="Bruno Lima", login="bruno123456789",
        email="bruno@example.com", senha="curta",
        telefone="83988880000", matricula="2026002"
    ), "Usuário 02:")

    restaurante = tentar_cadastrar_restaurante(fachada, DadosRestaurante(
        nome="Restaurante do CI", descricao="Almoços no campus",
        localizacao="Centro de Informática", telefone="83977770000",
        horario_limite_agendamento=time(10, 0)
    ), "Restaurante 01:")

    if restaurante is not None:
        tentar_cadastrar_usuario(fachada, DadosUsuario(
            perfil="gestor_restaurante", nome="Carlos Souza", login="carlossouza",
            email="carlos@example.com", senha="Senha@2026",
            telefone="83966660000", restaurante_id=restaurante.id
        ), "Usuário 03:")

        print("\n=========================================\n2 - REMOÇÃO DE RESTAURANTE\n=========================================\n")
        tentar_remover_restaurante(fachada, restaurante.id)


    print("\n=========================================\n3 - TESTE DE ATUALIZAÇÃO DE USUÁRIOS\n=========================================\n")
    
    tentar_atualizar_usuario(fachada, 1, DadosUsuario(
        perfil="estudante", nome="Ana Oliveira", login="anasilva",
        email="ana.oli@example.com", senha="NovaSenha@2026",
        telefone="83999990000", matricula="2026001"
    ), "Atualização 01:")

    # Falso positivo: Atualizando Ana sem mudar login/email
    tentar_atualizar_usuario(fachada, 1, DadosUsuario(
        perfil="estudante", nome="Ana Silva de Oliveira", login="anasilva",
        email="ana.oli@example.com", senha="NovaSenha@2026",
        telefone="83999990000", matricula="2026001"
    ), "Atualização 02:")


    print("\n=========================================\n4 - TESTE DE REMOÇÃO DE USUÁRIO\n=========================================\n")
    
    tentar_cadastrar_usuario(fachada, DadosUsuario(
        perfil="estudante", nome="Usuario Temporario", login="tempuser",
        email="temp@example.com", senha="Senha@2026",
        telefone="83900000000", matricula="2026999"
    ), "Usuário 04:")

    tentar_remover_usuario(fachada, 3, 'Removendo "tempuser":')
    tentar_remover_usuario(fachada, 999, "Removendo id Inexistente:")


# Relatório Final

def exibir_relatorio_final(fachada: FacadeSingletonController) -> None:
    print("\n=========================================\n5 - LISTAGEM DE ENTIDADES\n=========================================")
    try:
        usuarios = fachada.listar_usuarios()
        restaurantes = fachada.listar_restaurantes()
    except ErroPersistenciaBase as erro:
        print(f"Falha de persistência ao listar: {erro}")
        return

    print("Usuários armazenados:")
    for usuario in usuarios:
        print(f"  [{usuario.id}] {usuario.perfil} | {usuario.login} | {usuario.email}")

    print("\nRestaurantes armazenados:")
    for item in restaurantes:
        print(f"  [{item.id}] {item.nome} | {item.localizacao}")

    print("\n--- Resumo de Entidades ---")
    print(f"Usuários cadastrados: {fachada.contar_usuarios()}")
    print(f"Restaurantes cadastrados: {fachada.contar_restaurantes()}")
    print(f"Total de entidades cadastradas: {fachada.contar_total_entidades()}")

    print("\n--- Relatório de Acessos ---")
    tentar_gerar_relatorio_acessos(fachada, "csv")
    tentar_gerar_relatorio_acessos(fachada, "html")
    tentar_gerar_relatorio_acessos(fachada, "pdf")



# MENUS INTERATIVOS

def menu_interativo_usuarios(fachada: FacadeSingletonController) -> None:
    while True:
        print("\n--- GERENCIAR USUÁRIOS ---")
        print("[ 1 ] Listar Todos")
        print("[ 2 ] Cadastrar Novo")
        print("[ 3 ] Buscar por ID")
        print("[ 4 ] Atualizar Existente")
        print("[ 5 ] Remover")
        print("[ 0 ] Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '0':
            break
            
        elif opcao == '1':
            print("\nUsuários cadastrados:")
            for u in fachada.listar_usuarios():
                print(f"  [{u.id}] {u.nome} ({u.perfil})")

        elif opcao == '2':
            # Lógica de cadastro (reaproveitada do que você já possui)
            print("\n(Funcionalidade de cadastro conectada aqui...)")

        elif opcao == '3':
            id_busca = int(input("\nID do usuário: "))
            try:
                usuario = fachada.buscar_usuario(id_busca)
                imprimir_detalhes_usuario(usuario, titulo=f"Detalhes do Usuário {usuario.id}:")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == '4':
            try:
                id_atualizar = int(input("\nID do usuário a atualizar: "))
                usr = fachada.buscar_usuario(id_atualizar)
                
                print(f"\nAtualizando: {usr.nome}")
                print("(Pressione ENTER para manter o valor atual)")
                
                # Atualização Inteligente: Se bater ENTER, mantém usr.campo
                novo_nome = input(f"Nome [{usr.nome}]: ").strip() or usr.nome
                novo_email = input(f"E-mail [{usr.email}]: ").strip() or usr.email
                novo_tel = input(f"Telefone [{formatar_telefone(usr.telefone)}]: ").strip() or usr.telefone
                nova_senha = input("Nova Senha [***]: ").strip() or getattr(usr, 'senha', '')
                
                dados_atualizados = DadosUsuario(
                    perfil=usr.perfil,  # Imutável via edição básica
                    nome=novo_nome,
                    login=usr.login,    # Imutável via edição básica
                    email=novo_email,
                    senha=nova_senha,
                    telefone=novo_tel,
                    matricula=getattr(usr, 'matricula', None),
                    restaurante_id=getattr(usr, 'restaurante_id', None)
                )
                
                fachada.atualizar_usuario(id_atualizar, dados_atualizados)
                print("\nUsuário atualizado com sucesso!")
            except ValueError as e:
                print(f"\nErro na atualização: {e}")

        elif opcao == '5':
            try:
                id_remover = int(input("\nID do usuário a remover: "))
                fachada.remover_usuario(id_remover)
                print("Usuário removido.")
            except ValueError as e:
                print(f"Erro: {e}")
        else:
            print("Opção inválida.")


def menu_interativo_restaurantes(fachada: FacadeSingletonController) -> None:
    # A estrutura aqui será idêntica à de usuários, chamando os métodos de Restaurante
    print("\n(Submenu de Restaurantes em construção...)")


def menu_principal(fachada: FacadeSingletonController) -> None:
    while True:
        print("\n" + "="*40)
        print("       SISTEMA GESTOR DE ALMOÇOS")
        print("="*40)
        print("[ 1 ] Gerenciar Usuários")
        print("[ 2 ] Gerenciar Restaurantes")
        print("[ 0 ] Sair do Sistema")
        print("="*40)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '0':
            print("Saindo...")
            break
        elif opcao == '1':
            menu_interativo_usuarios(fachada)
        elif opcao == '2':
            menu_interativo_restaurantes(fachada)
        else:
            print("Opção inválida!")


def main():
    argumentos = ler_argumentos()

    fabrica = escolher_fabrica(argumentos)

    try:
        fachada = FacadeSingletonController.obter_instancia(
            fabrica.criar_repositorio_usuarios(),
            fabrica.criar_repositorio_restaurantes(),
            fabrica.criar_repositorio_acessos(),
            criar_adaptador_logging(),
        )
    except ErroPersistenciaBase as erro:
        print(f"Não foi possível iniciar o armazenamento: {erro}")
        return

    print(f"Armazenamento: {argumentos.armazenamento}")
    
    mesma_fachada = FacadeSingletonController.obter_instancia() is fachada
    print(f"Mesma instância da fachada: {mesma_fachada}\n")

    executar_cenario_demonstracao(fachada)
    exibir_relatorio_final(fachada)

    menu_principal(fachada)


if __name__ == "__main__":
    main()