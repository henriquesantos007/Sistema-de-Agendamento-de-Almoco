from pathlib import Path
from typing import Optional, Union

from source.dominio.restaurantes import RepositorioRestaurantes
from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios
from source.infraestrutura.persistencia.arquivo import (
    RepositorioRestaurantesArquivo,
    RepositorioUsuariosArquivo,
)
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
    RepositorioUsuariosMemoria,
)

ARMAZENAMENTOS = ("memoria", "arquivo")

_CAMINHOS_PADRAO = {
    "usuarios": "dados/usuarios.bin",
    "restaurantes": "dados/restaurantes.bin",
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
        return RepositorioUsuariosArquivo(
            caminho or _CAMINHOS_PADRAO["usuarios"]
        )

    raise ValueError(
        f"armazenamento invalido: {armazenamento!r} "
        f"(opcoes: {', '.join(ARMAZENAMENTOS)})"
    )


def criar_repositorio_restaurantes(
    armazenamento: str = "memoria",
    caminho: Optional[Union[str, Path]] = None,
) -> RepositorioRestaurantes:
    """Escolhe o mecanismo de persistencia dos restaurantes."""
    armazenamento = (armazenamento or "").strip().lower()

    if armazenamento == "memoria":
        return RepositorioRestaurantesMemoria()
    if armazenamento == "arquivo":
        return RepositorioRestaurantesArquivo(
            caminho or _CAMINHOS_PADRAO["restaurantes"]
        )

    raise ValueError(
        f"armazenamento invalido: {armazenamento!r} "
        f"(opcoes: {', '.join(ARMAZENAMENTOS)})"
    )