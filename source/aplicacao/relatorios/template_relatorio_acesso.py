from abc import ABC, abstractmethod
from collections import Counter

from source.aplicacao.relatorios.estatisticas_acesso import (
    USUARIO_REMOVIDO,
    AcessosPorUsuario,
    Documento,
    EstatisticasAcesso,
)
from source.dominio.acessos import RepositorioAcessos
from source.dominio.usuarios import RepositorioUsuarios


class TemplateRelatorioAcesso(ABC):
    """Template Method do relatorio de acessos (ADR-0011).

    gerar() fixa o fluxo: obtem as estatisticas, calculadas uma unica vez
    aqui, e entrega a formatacao a subclasse de cada formato.
    """

    def __init__(
        self,
        repositorio_acessos: RepositorioAcessos,
        repositorio_usuarios: RepositorioUsuarios,
    ) -> None:
        self._repositorio_acessos = repositorio_acessos
        self._repositorio_usuarios = repositorio_usuarios

    def gerar(self) -> Documento:
        return self.formatar(self.obter_estatisticas())

    def obter_estatisticas(self) -> EstatisticasAcesso:
        registros = self._repositorio_acessos.listar_todos()
        acessos_por_usuario = Counter(registro.usuario_id for registro in registros)

        detalhamento = sorted(
            (
                self._detalhar(usuario_id, quantidade)
                for usuario_id, quantidade in acessos_por_usuario.items()
            ),
            key=lambda linha: (-linha.quantidade, linha.usuario_id),
        )

        return EstatisticasAcesso(
            total_acessos=len(registros),
            usuarios_distintos=len(acessos_por_usuario),
            detalhamento=tuple(detalhamento),
        )

    def _detalhar(self, usuario_id: int, quantidade: int) -> AcessosPorUsuario:
        usuario = self._repositorio_usuarios.buscar_por_id(usuario_id)
        if usuario is None:
            # RF16: acessos de usuario removido continuam contando.
            return AcessosPorUsuario(
                usuario_id, USUARIO_REMOVIDO, USUARIO_REMOVIDO, quantidade
            )
        return AcessosPorUsuario(usuario_id, usuario.login, usuario.perfil, quantidade)

    @abstractmethod
    def formatar(self, estatisticas: EstatisticasAcesso) -> Documento:
        raise NotImplementedError
