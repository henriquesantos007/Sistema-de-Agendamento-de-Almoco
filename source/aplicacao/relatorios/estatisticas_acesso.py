from dataclasses import dataclass
from typing import Tuple

USUARIO_REMOVIDO = "usuário removido"


@dataclass(frozen=True)
class AcessosPorUsuario:
    usuario_id: int
    login: str
    perfil: str
    quantidade: int


@dataclass(frozen=True)
class EstatisticasAcesso:
    total_acessos: int
    usuarios_distintos: int
    detalhamento: Tuple[AcessosPorUsuario, ...]


@dataclass(frozen=True)
class Documento:
    """Conteudo textual de um relatorio, gerado no formato pedido."""

    formato: str
    conteudo: str
