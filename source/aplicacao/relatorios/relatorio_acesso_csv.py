import csv
import io

from source.aplicacao.relatorios.estatisticas_acesso import (
    Documento,
    EstatisticasAcesso,
)
from source.aplicacao.relatorios.template_relatorio_acesso import (
    TemplateRelatorioAcesso,
)

FORMATO_CSV = "csv"

_INICIOS_DE_FORMULA = ("=", "+", "-", "@", "\t", "\r")
_PREFIXO_TEXTO = "'"


class RelatorioAcessoCSV(TemplateRelatorioAcesso):
    """Gera dois blocos separados por uma linha em branco: resumo e detalhamento."""

    def formatar(self, estatisticas: EstatisticasAcesso) -> Documento:
        saida = io.StringIO()
        escritor = csv.writer(saida, lineterminator="\n")

        escritor.writerow(["total_acessos", "usuarios_distintos"])
        escritor.writerow(
            [estatisticas.total_acessos, estatisticas.usuarios_distintos]
        )
        escritor.writerow([])
        escritor.writerow(["usuario_id", "login", "perfil", "quantidade"])
        for linha in estatisticas.detalhamento:
            escritor.writerow(
                [
                    linha.usuario_id,
                    self._neutralizar_formula(linha.login),
                    self._neutralizar_formula(linha.perfil),
                    linha.quantidade,
                ]
            )

        return Documento(formato=FORMATO_CSV, conteudo=saida.getvalue())

    @staticmethod
    def _neutralizar_formula(texto: str) -> str:
        """Impede que planilhas interpretem o texto como formula ao abrir o CSV."""
        if texto.startswith(_INICIOS_DE_FORMULA):
            return _PREFIXO_TEXTO + texto
        return texto
