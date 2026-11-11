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
                [linha.usuario_id, linha.login, linha.perfil, linha.quantidade]
            )

        return Documento(formato=FORMATO_CSV, conteudo=saida.getvalue())
