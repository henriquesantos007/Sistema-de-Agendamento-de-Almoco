from typing import List

from source.dominio.acessos import RegistroAcesso, RepositorioAcessos


class RepositorioAcessosMemoria(RepositorioAcessos):
    def __init__(self) -> None:
        self._registros: List[RegistroAcesso] = []

    def registrar(self, acesso: RegistroAcesso) -> None:
        self._registros.append(acesso)

    def listar_todos(self) -> List[RegistroAcesso]:
        return list(self._registros)
