import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Union

from source.dominio.acessos import (
    ErroPersistencia,
    RegistroAcesso,
    RepositorioAcessos,
)

_CODIFICACAO = "utf-8"
_CAMPO_USUARIO = "usuario_id"
_CAMPO_INSTANTE = "instante"


class RepositorioAcessosArquivo(RepositorioAcessos):
    """Persiste registros de acesso por acrescimo, uma linha JSON por registro.

    Ao contrario dos repositorios de usuarios e restaurantes, nao herda da
    versao em memoria nem regrava o arquivo: registros de acesso so crescem e
    nunca sao editados, entao cada registro e apenas acrescentado ao fim.
    """

    def __init__(self, caminho: Union[str, Path]) -> None:
        self._caminho = Path(caminho)

    def registrar(self, acesso: RegistroAcesso) -> None:
        linha = json.dumps(
            {
                _CAMPO_USUARIO: acesso.usuario_id,
                _CAMPO_INSTANTE: acesso.instante.isoformat(),
            }
        )

        try:
            self._caminho.parent.mkdir(parents=True, exist_ok=True)
            with self._caminho.open(
                "a", encoding=_CODIFICACAO, newline="\n"
            ) as arquivo:
                arquivo.write(linha + "\n")
                arquivo.flush()
                os.fsync(arquivo.fileno())
        except OSError as erro:
            raise ErroPersistencia(
                f"nao foi possivel gravar o arquivo '{self._caminho}': {erro}"
            ) from erro

    def listar_todos(self) -> List[RegistroAcesso]:
        if not self._caminho.exists():
            return []

        try:
            with self._caminho.open(
                "r", encoding=_CODIFICACAO, newline="\n"
            ) as arquivo:
                linhas = arquivo.read().splitlines()
        except (OSError, UnicodeDecodeError) as erro:
            raise ErroPersistencia(
                f"nao foi possivel ler o arquivo '{self._caminho}': {erro}"
            ) from erro

        return [
            self._interpretar(linha, numero)
            for numero, linha in enumerate(linhas, start=1)
        ]

    def _interpretar(self, linha: str, numero: int) -> RegistroAcesso:
        try:
            conteudo = json.loads(linha)
            if not isinstance(conteudo, dict):
                raise ValueError("a linha nao contem um objeto")
            instante = conteudo[_CAMPO_INSTANTE]
            if not isinstance(instante, str):
                raise ValueError("instante precisa ser um texto em ISO 8601")
            return RegistroAcesso(
                usuario_id=conteudo[_CAMPO_USUARIO],
                instante=datetime.fromisoformat(instante),
            )
        except (KeyError, ValueError) as erro:
            raise ErroPersistencia(
                f"arquivo '{self._caminho}' corrompido ou em formato invalido "
                f"na linha {numero}: {erro}"
            ) from erro
