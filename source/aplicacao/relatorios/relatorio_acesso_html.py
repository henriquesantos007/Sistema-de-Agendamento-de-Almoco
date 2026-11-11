from html import escape

from source.aplicacao.relatorios.estatisticas_acesso import (
    Documento,
    EstatisticasAcesso,
)
from source.aplicacao.relatorios.template_relatorio_acesso import (
    TemplateRelatorioAcesso,
)

FORMATO_HTML = "html"

_TITULO = "Relatório de Acessos"


class RelatorioAcessoHTML(TemplateRelatorioAcesso):
    def formatar(self, estatisticas: EstatisticasAcesso) -> Documento:
        linhas = "\n".join(
            "      <tr>"
            f"<td>{linha.usuario_id}</td>"
            f"<td>{escape(linha.login)}</td>"
            f"<td>{escape(linha.perfil)}</td>"
            f"<td>{linha.quantidade}</td>"
            "</tr>"
            for linha in estatisticas.detalhamento
        )
        corpo_detalhamento = f"\n{linhas}\n    " if linhas else ""

        conteudo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>{_TITULO}</title>
</head>
<body>
  <h1>{_TITULO}</h1>
  <table id="resumo">
    <tr><th>Total de acessos</th><td>{estatisticas.total_acessos}</td></tr>
    <tr><th>Usuários distintos</th><td>{estatisticas.usuarios_distintos}</td></tr>
  </table>
  <table id="detalhamento">
    <thead>
      <tr><th>Id</th><th>Login</th><th>Perfil</th><th>Acessos</th></tr>
    </thead>
    <tbody>{corpo_detalhamento}</tbody>
  </table>
</body>
</html>
"""
        return Documento(formato=FORMATO_HTML, conteudo=conteudo)
