from typing import Callable, Dict

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.dominio.usuarios.perfil import Perfil
from source.dominio.usuarios.usuario import (
    Administrador,
    DadosBasicosUsuario,
    Estudante,
    GestorRestaurante,
    Usuario,
)

Criador = Callable[[DadosBasicosUsuario, DadosUsuario], Usuario]


def _criar_estudante(basicos: DadosBasicosUsuario, dados: DadosUsuario) -> Usuario:
    return Estudante(basicos, matricula=dados.matricula or "")


def _criar_gestor(basicos: DadosBasicosUsuario, dados: DadosUsuario) -> Usuario:
    return GestorRestaurante(basicos, restaurante_id=dados.restaurante_id)


def _criar_administrador(basicos: DadosBasicosUsuario, dados: DadosUsuario) -> Usuario:
    return Administrador(basicos)


class FabricaUsuario:
    """Factory Method: cada perfil registra como o seu usuario e construido."""

    _CRIADORES: Dict[Perfil, Criador] = {
        Perfil.ESTUDANTE: _criar_estudante,
        Perfil.GESTOR_RESTAURANTE: _criar_gestor,
        Perfil.ADMINISTRADOR: _criar_administrador,
    }

    def criar(
        self, perfil: Perfil, basicos: DadosBasicosUsuario, dados: DadosUsuario
    ) -> Usuario:
        return self._CRIADORES[perfil](basicos, dados)
