from pathlib import Path
from typing import Optional, Union

from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios
from source.infraestrutura.persistencia.arquivo import RepositorioUsuariosArquivo
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria

ARMAZENAMENTOS = ("memoria", "arquivo", "sqlite")

_CAMINHOS_PADRAO = {
    "arquivo": "dados/usuarios.bin"
}


def criar_repositorio_usuarios(
    armazenamento: str = "memoria",
    caminho: Optional[Union[str, Path]] = None,
) -> RepositorioUsuarios:
    """Escolhe o mecanismo de persistencia no inicio da execucao.

    Pode levantar ErroPersistencia se o arquivo/banco nao puder ser aberto.
    """
    armazenamento = (armazenamento or "").strip().lower()

    if armazenamento == "memoria":
        return RepositorioUsuariosMemoria()
    if armazenamento == "arquivo":
        return RepositorioUsuariosArquivo(caminho or _CAMINHOS_PADRAO["arquivo"])

    raise ValueError(
        f"armazenamento invalido: {armazenamento!r} "
        f"(opcoes: {', '.join(ARMAZENAMENTOS)})"
    )