import pytest

from source.aplicacao.fachada.facade_singleton_controller import FacadeSingletonController
from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.infraestrutura.persistencia.memoria.repositorio_usuarios_memoria import RepositorioUsuariosMemoria
from source.infraestrutura.persistencia.memoria.repositorio_restaurantes_memoria import RepositorioRestaurantesMemoria
from source.infraestrutura.persistencia.memoria.repositorio_acessos_memoria import RepositorioAcessosMemoria
from source.infraestrutura.logs import criar_adaptador_logging


@pytest.fixture
def fachada_configurada():
    """Configura uma instância limpa da Fachada em memória para cada teste."""
    FacadeSingletonController.reiniciar()
    fachada = FacadeSingletonController.obter_instancia(
        RepositorioUsuariosMemoria(),
        RepositorioRestaurantesMemoria(),
        RepositorioAcessosMemoria(),
        criar_adaptador_logging()
    )
    yield fachada
    FacadeSingletonController.reiniciar()


def test_deve_desfazer_ultima_atualizacao_restaurando_estado_original(fachada_configurada):
    # ==========================================
    # 1. ARRANGE (Preparação)
    # ==========================================
    fachada = fachada_configurada
    
    # Cadastra um usuário inicial
    dados_iniciais = DadosUsuario(
        perfil="estudante", nome="Ana Original", login="anasilva",
        email="ana@example.com", senha="Senha@123",
        telefone="83999999999", matricula="2026001"
    )
    usuario = fachada.cadastrar_usuario(dados_iniciais)
    id_usuario = usuario.id

    # Prepara os dados para a atualização
    dados_atualizados = DadosUsuario(
        perfil="estudante", nome="Ana Modificada", login="anasilva",
        email="ana.mod@example.com", senha="Senha@123",
        telefone="83900000000", matricula="2026001"
    )

    # ==========================================
    # 2. ACT (Ação)
    # ==========================================
    # Executa a atualização (o Command vai tirar o Memento aqui)
    fachada.atualizar_usuario(id_usuario, dados_atualizados)
    
    # Verifica se realmente atualizou antes de desfazer
    usr_apos_atualizacao = fachada.buscar_usuario(id_usuario)
    assert usr_apos_atualizacao.nome == "Ana Modificada"
    assert usr_apos_atualizacao.email == "ana.mod@example.com"

    # Dispara o gatilho de desfazer (Zelador chama o Command.desfazer)
    resultado_desfazer = fachada.desfazer_ultima_atualizacao_usuario()

    # ==========================================
    # 3. ASSERT (Verificação)
    # ==========================================
    assert resultado_desfazer is True
    
    # Busca novamente no repositório para garantir que persistiu a reversão
    usr_revertido = fachada.buscar_usuario(id_usuario)
    
    # O estado deve ser exatamente igual ao `dados_iniciais`
    assert usr_revertido.nome == "Ana Original"
    assert usr_revertido.email == "ana@example.com"
    assert usr_revertido.telefone == "83999999999"


def test_nao_deve_desfazer_se_o_historico_estiver_vazio(fachada_configurada):
    # ==========================================
    # 1. ARRANGE (Preparação)
    # ==========================================
    fachada = fachada_configurada
    # Nenhuma atualização foi feita no sistema...

    # ==========================================
    # 2. ACT (Ação)
    # ==========================================
    resultado = fachada.desfazer_ultima_atualizacao_usuario()

    # ==========================================
    # 3. ASSERT (Verificação)
    # ==========================================
    # Deve retornar False graciosamente, sem quebrar o sistema
    assert resultado is False


def test_deve_desfazer_somente_a_ultima_de_duas_atualizacoes(fachada_configurada):
    fachada = fachada_configurada
    usuario = fachada.cadastrar_usuario(DadosUsuario(
        perfil="estudante", nome="Ana Original", login="anasilva",
        email="ana@example.com", senha="Senha@123",
        telefone="83999999999", matricula="2026001"
    ))

    dados_primeira_atualizacao = DadosUsuario(
        perfil="estudante", nome="Ana Primeira", login="anasilva",
        email="ana.primeira@example.com", senha="Senha@123",
        telefone="83900000000", matricula="2026001"
    )
    dados_segunda_atualizacao = DadosUsuario(
        perfil="estudante", nome="Ana Segunda", login="anasilva",
        email="ana.segunda@example.com", senha="Senha@123",
        telefone="83911111111", matricula="2026001"
    )

    fachada.atualizar_usuario(usuario.id, dados_primeira_atualizacao)
    fachada.atualizar_usuario(usuario.id, dados_segunda_atualizacao)

    assert fachada.desfazer_ultima_atualizacao_usuario() is True
    usuario_revertido = fachada.buscar_usuario(usuario.id)
    assert usuario_revertido.nome == "Ana Primeira"
    assert usuario_revertido.email == "ana.primeira@example.com"
    assert usuario_revertido.telefone == "83900000000"

    assert fachada.desfazer_ultima_atualizacao_usuario() is False
    assert fachada.buscar_usuario(usuario.id).nome == "Ana Primeira"


def test_atualizacao_invalida_nao_descarta_historico_da_ultima_atualizacao_valida(
    fachada_configurada,
):
    fachada = fachada_configurada
    usuario = fachada.cadastrar_usuario(DadosUsuario(
        perfil="estudante", nome="Ana Original", login="anasilva",
        email="ana@example.com", senha="Senha@123",
        telefone="83999999999", matricula="2026001"
    ))
    dados_atualizados = DadosUsuario(
        perfil="estudante", nome="Ana Modificada", login="anasilva",
        email="ana.mod@example.com", senha="Senha@123",
        telefone="83900000000", matricula="2026001"
    )
    dados_invalidos = DadosUsuario(
        perfil="estudante", nome="", login="anasilva",
        email="ana.invalid@example.com", senha="Senha@123",
        telefone="83900000000", matricula="2026001"
    )
    fachada.atualizar_usuario(usuario.id, dados_atualizados)

    with pytest.raises(ValueError, match="Erros de validação"):
        fachada.atualizar_usuario(usuario.id, dados_invalidos)

    assert fachada.buscar_usuario(usuario.id).nome == "Ana Modificada"
    assert fachada.desfazer_ultima_atualizacao_usuario() is True
    assert fachada.buscar_usuario(usuario.id).nome == "Ana Original"


def test_remover_usuario_invalida_o_desfazimento_desse_usuario(
    fachada_configurada,
):
    fachada = fachada_configurada
    usuario = fachada.cadastrar_usuario(DadosUsuario(
        perfil="estudante",
        nome="Ana Original",
        login="anasilva",
        email="ana@example.com",
        senha="Senha@123",
        telefone="83999999999",
        matricula="2026001",
    ))
    dados_atualizados = DadosUsuario(
        perfil="estudante",
        nome="Ana Modificada",
        login="anasilva",
        email="ana.mod@example.com",
        senha="Senha@123",
        telefone="83900000000",
        matricula="2026001",
    )

    fachada.atualizar_usuario(usuario.id, dados_atualizados)
    fachada.remover_usuario(usuario.id)

    assert fachada.desfazer_ultima_atualizacao_usuario() is False