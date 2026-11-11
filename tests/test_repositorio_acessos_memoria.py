from datetime import datetime, timezone

from source.dominio.acessos import RegistroAcesso, RepositorioAcessos
from source.infraestrutura.persistencia.memoria import RepositorioAcessosMemoria


def registro(usuario_id, minuto=0):
    return RegistroAcesso(
        usuario_id=usuario_id,
        instante=datetime(2026, 11, 10, 12, minuto, tzinfo=timezone.utc),
    )


def test_deve_implementar_o_contrato_do_dominio():
    assert isinstance(RepositorioAcessosMemoria(), RepositorioAcessos)


def test_repositorio_novo_nao_deve_ter_registros():
    assert RepositorioAcessosMemoria().listar_todos() == []


def test_deve_listar_os_registros_na_ordem_em_que_foram_registrados():
    repositorio = RepositorioAcessosMemoria()
    registros = [registro(2, 5), registro(1, 1), registro(2, 3)]

    for item in registros:
        repositorio.registrar(item)

    assert repositorio.listar_todos() == registros


def test_alterar_a_lista_devolvida_nao_deve_afetar_o_repositorio():
    repositorio = RepositorioAcessosMemoria()
    repositorio.registrar(registro(1))

    repositorio.listar_todos().clear()

    assert len(repositorio.listar_todos()) == 1
