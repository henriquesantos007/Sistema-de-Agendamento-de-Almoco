import pytest

from source.dominio.usuarios.usuario import Administrador
from source.infraestrutura.persistencia.arquivo import RepositorioUsuariosArquivo
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria


def novo_admin(indice):
    return Administrador(
        nome=f"Admin {indice}",
        login=f"admin{indice}",
        email=f"admin{indice}@example.com",
        senha="hash",
        telefone=f"8399999000{indice}",
    )


@pytest.fixture(params=["memoria", "arquivo"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        return RepositorioUsuariosMemoria()
    return RepositorioUsuariosArquivo(tmp_path / "usuarios.bin")


def test_repositorio_vazio_deve_contar_zero(repositorio):
    assert repositorio.contar() == 0


def test_deve_contar_usuarios_adicionados(repositorio):
    repositorio.adicionar(novo_admin(1))
    repositorio.adicionar(novo_admin(2))

    assert repositorio.contar() == 2


def test_arquivo_deve_contar_usuarios_apos_reabrir(tmp_path):
    caminho = tmp_path / "usuarios.bin"
    RepositorioUsuariosArquivo(caminho).adicionar(novo_admin(1))

    assert RepositorioUsuariosArquivo(caminho).contar() == 1
