"""Apoio compartilhado pelos testes de relatorios de acesso."""

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from source.aplicacao.logger_aplicacao import LoggerAplicacao, NivelEvento
from source.dominio.acessos import RegistroAcesso
from source.dominio.usuarios import Administrador, Estudante, Usuario
from source.infraestrutura.persistencia.memoria import RepositorioAcessosMemoria


class UsuariosCadastrados:
    """Substituto de RepositorioUsuarios com ids escolhidos pelo teste."""

    def __init__(self, usuarios: List[Usuario]) -> None:
        self._usuarios = {usuario.id: usuario for usuario in usuarios}
        self.consultas: List[int] = []

    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        self.consultas.append(id_usuario)
        return self._usuarios.get(id_usuario)


class LoggerEmMemoria(LoggerAplicacao):
    def __init__(self) -> None:
        self.eventos: List[Tuple[str, str, NivelEvento]] = []

    def registrar(
        self,
        evento: str,
        detalhes: str,
        nivel: NivelEvento = NivelEvento.INFORMACAO,
    ) -> None:
        self.eventos.append((evento, detalhes, nivel))


def estudante(id: int, login: str) -> Estudante:
    return Estudante(
        nome=f"Nome de {login}",
        login=login,
        email=f"{login}@example.com",
        senha="Senha@2026",
        telefone=f"8399999{id:04d}",
        matricula=f"2026{id:03d}",
        id=id,
    )


def administrador(id: int, login: str) -> Administrador:
    return Administrador(
        nome=f"Nome de {login}",
        login=login,
        email=f"{login}@example.com",
        senha="Senha@2026",
        telefone=f"8388888{id:04d}",
        id=id,
    )


def acessos_de(*usuario_ids: int) -> RepositorioAcessosMemoria:
    repositorio = RepositorioAcessosMemoria()
    for minuto, usuario_id in enumerate(usuario_ids):
        repositorio.registrar(
            RegistroAcesso(
                usuario_id=usuario_id,
                instante=datetime(2026, 11, 10, 12, minuto, tzinfo=timezone.utc),
            )
        )
    return repositorio
