from typing import Dict, Type

from source.aplicacao.logger_aplicacao import LoggerAplicacao, NivelEvento
from source.aplicacao.relatorios.estatisticas_acesso import Documento
from source.aplicacao.relatorios.excecoes import FormatoRelatorioInvalido
from source.aplicacao.relatorios.relatorio_acesso_csv import (
    FORMATO_CSV,
    RelatorioAcessoCSV,
)
from source.aplicacao.relatorios.relatorio_acesso_html import (
    FORMATO_HTML,
    RelatorioAcessoHTML,
)
from source.aplicacao.relatorios.template_relatorio_acesso import (
    TemplateRelatorioAcesso,
)
from source.dominio.acessos import RepositorioAcessos
from source.dominio.excecoes import ErroPersistenciaBase
from source.dominio.usuarios import RepositorioUsuarios

_RELATORIOS: Dict[str, Type[TemplateRelatorioAcesso]] = {
    FORMATO_HTML: RelatorioAcessoHTML,
    FORMATO_CSV: RelatorioAcessoCSV,
}

FORMATOS_ACEITOS = tuple(formato.upper() for formato in _RELATORIOS)

EVENTO_GERADO = "relatorio_acessos_gerado"
EVENTO_RECUSADO = "relatorio_acessos_recusado"
EVENTO_FALHOU = "relatorio_acessos_falhou"


class ServicoRelatorioAcesso:
    def __init__(
        self,
        repositorio_acessos: RepositorioAcessos,
        repositorio_usuarios: RepositorioUsuarios,
        logger: LoggerAplicacao,
    ) -> None:
        self._repositorio_acessos = repositorio_acessos
        self._repositorio_usuarios = repositorio_usuarios
        self._logger = logger

    def gerar(self, formato: str) -> Documento:
        formato_normalizado = self._normalizar(formato)
        classe_relatorio = _RELATORIOS.get(formato_normalizado)

        if classe_relatorio is None:
            # O formato pedido e entrada livre: nao vai para o log.
            self._logger.registrar(
                EVENTO_RECUSADO,
                "formato nao suportado; formatos aceitos: "
                + ", ".join(FORMATOS_ACEITOS),
                NivelEvento.AVISO,
            )
            raise FormatoRelatorioInvalido(FORMATOS_ACEITOS)

        relatorio = classe_relatorio(
            self._repositorio_acessos, self._repositorio_usuarios
        )
        try:
            documento = relatorio.gerar()
        except ErroPersistenciaBase:
            self._logger.registrar(
                EVENTO_FALHOU,
                f"formato={formato_normalizado}; falha de persistencia",
                NivelEvento.ERRO,
            )
            raise

        self._logger.registrar(
            EVENTO_GERADO, f"formato={formato_normalizado}; relatorio gerado"
        )
        return documento

    @staticmethod
    def _normalizar(formato: object) -> str:
        return formato.strip().lower() if isinstance(formato, str) else ""
