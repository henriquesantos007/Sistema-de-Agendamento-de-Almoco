from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from source.dominio.acessos import RepositorioAcessos
from source.dominio.restaurantes import RepositorioRestaurantes
from source.dominio.usuarios import RepositorioUsuarios
from source.infraestrutura.persistencia.arquivo import (
    RepositorioAcessosArquivo,
    RepositorioRestaurantesArquivo,
    RepositorioUsuariosArquivo,
)
from source.infraestrutura.persistencia.memoria import (
    RepositorioAcessosMemoria,
    RepositorioRestaurantesMemoria,
    RepositorioUsuariosMemoria,
)

Caminho = Union[str, Path]

CAMINHO_PADRAO_USUARIOS = "dados/usuarios.bin"
CAMINHO_PADRAO_RESTAURANTES = "dados/restaurantes.bin"
CAMINHO_PADRAO_ACESSOS = "dados/acessos.jsonl"


class FabricaRepositorios(ABC):
    """Abstract Factory da familia de repositorios de um mecanismo.

    Cada fabrica concreta cria todos os repositorios no mesmo mecanismo de
    persistencia, o que impede combinar mecanismos diferentes por engano.
    Os metodos podem levantar ErroPersistencia se o armazenamento nao puder
    ser aberto.
    """

    @abstractmethod
    def criar_repositorio_usuarios(self) -> RepositorioUsuarios:
        raise NotImplementedError

    @abstractmethod
    def criar_repositorio_restaurantes(self) -> RepositorioRestaurantes:
        raise NotImplementedError

    @abstractmethod
    def criar_repositorio_acessos(self) -> RepositorioAcessos:
        raise NotImplementedError


class FabricaRepositoriosMemoria(FabricaRepositorios):
    def criar_repositorio_usuarios(self) -> RepositorioUsuarios:
        return RepositorioUsuariosMemoria()

    def criar_repositorio_restaurantes(self) -> RepositorioRestaurantes:
        return RepositorioRestaurantesMemoria()

    def criar_repositorio_acessos(self) -> RepositorioAcessos:
        return RepositorioAcessosMemoria()


class FabricaRepositoriosArquivo(FabricaRepositorios):
    def __init__(
        self,
        caminho_usuarios: Optional[Caminho] = None,
        caminho_restaurantes: Optional[Caminho] = None,
        caminho_acessos: Optional[Caminho] = None,
    ) -> None:
        self._caminho_usuarios = Path(caminho_usuarios or CAMINHO_PADRAO_USUARIOS)
        self._caminho_restaurantes = Path(
            caminho_restaurantes or CAMINHO_PADRAO_RESTAURANTES
        )
        self._caminho_acessos = Path(caminho_acessos or CAMINHO_PADRAO_ACESSOS)

    def criar_repositorio_usuarios(self) -> RepositorioUsuarios:
        return RepositorioUsuariosArquivo(self._caminho_usuarios)

    def criar_repositorio_restaurantes(self) -> RepositorioRestaurantes:
        return RepositorioRestaurantesArquivo(self._caminho_restaurantes)

    def criar_repositorio_acessos(self) -> RepositorioAcessos:
        return RepositorioAcessosArquivo(self._caminho_acessos)
