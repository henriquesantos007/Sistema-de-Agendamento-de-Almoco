from typing import List, Optional

from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios
from source.dominio.usuarios.usuario import Estudante, Usuario


class RepositorioUsuariosMemoria(RepositorioUsuarios):
    def __init__(self) -> None:
        self._usuarios: List[Usuario] = []
        self._proximo_id = 1

    def adicionar(self, usuario: Usuario) -> Usuario:
        usuario.id = self._proximo_id
        self._proximo_id += 1
        self._usuarios.append(usuario)
        return usuario

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        email_normalizado = email.strip().casefold()
        return next(
            (
                usuario
                for usuario in self._usuarios
                if usuario.email.strip().casefold() == email_normalizado
            ),
            None,
        )

    def existe_matricula(self, matricula: str) -> bool:
        matricula_normalizada = matricula.strip().casefold()
        return any(
            isinstance(usuario, Estudante)
            and usuario.matricula.strip().casefold() == matricula_normalizada
            for usuario in self._usuarios
        )

    def existe_telefone(self, telefone: str) -> bool:
        telefone_normalizado = telefone.strip()
        return any(
            isinstance(usuario, Estudante)
            and usuario.telefone.strip() == telefone_normalizado
            for usuario in self._usuarios
        )