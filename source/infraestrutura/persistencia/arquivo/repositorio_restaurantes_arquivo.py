import os
import pickle
from pathlib import Path
from typing import Union

from source.dominio.restaurantes import ErroPersistencia, Restaurante
from source.infraestrutura.persistencia.memoria import (
    RepositorioRestaurantesMemoria,
)

_VERSAO_FORMATO = 1


class RepositorioRestaurantesArquivo(RepositorioRestaurantesMemoria):
    """Persiste restaurantes em arquivo binario usando pickle."""

    def __init__(self, caminho: Union[str, Path]) -> None:
        super().__init__()
        self._caminho = Path(caminho)
        self._carregar()

    def adicionar(self, restaurante: Restaurante) -> Restaurante:
        proximo_id_anterior = self._proximo_id
        super().adicionar(restaurante)
        try:
            self._salvar()
        except ErroPersistencia:
            self._restaurantes.pop()
            self._proximo_id = proximo_id_anterior
            restaurante.id = None
            raise
        return restaurante

    def atualizar(self, restaurante: Restaurante) -> Restaurante:
        atualizado = super().atualizar(restaurante)
        try:
            self._salvar()
        except ErroPersistencia:
            self._carregar()
            raise
        return atualizado

    def remover(self, restaurante_id: int) -> bool:
        removido = super().remover(restaurante_id)
        if not removido:
            return False

        try:
            self._salvar()
        except ErroPersistencia:
            self._carregar()
            raise
        return True

    def _carregar(self) -> None:
        if not self._caminho.exists():
            return

        try:
            with self._caminho.open("rb") as arquivo:
                conteudo = pickle.load(arquivo)

            if not isinstance(conteudo, dict):
                raise ValueError("estrutura do arquivo nao reconhecida")

            restaurantes = conteudo.get("restaurantes")
            proximo_id = conteudo.get("proximo_id")
            if conteudo.get("versao") != _VERSAO_FORMATO:
                raise ValueError("estrutura do arquivo nao reconhecida")
            if not isinstance(restaurantes, list) or not all(
                isinstance(item, Restaurante) for item in restaurantes
            ):
                raise ValueError("estrutura do arquivo nao reconhecida")
            ids = [restaurante.id for restaurante in restaurantes]
            if (
                any(
                    type(restaurante_id) is not int or restaurante_id < 1
                    for restaurante_id in ids
                )
                or len(set(ids)) != len(restaurantes)
            ):
                raise ValueError("identificadores de restaurante invalidos")
            if (
                type(proximo_id) is not int
                or proximo_id <= max(ids, default=0)
            ):
                raise ValueError("estrutura do arquivo nao reconhecida")

            self._restaurantes = restaurantes
            self._proximo_id = proximo_id
        except OSError as erro:
            raise ErroPersistencia(
                f"nao foi possivel ler o arquivo '{self._caminho}': {erro}"
            ) from erro
        except (
            pickle.UnpicklingError,
            EOFError,
            AttributeError,
            ImportError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ) as erro:
            raise ErroPersistencia(
                f"arquivo '{self._caminho}' corrompido ou em formato invalido: {erro}"
            ) from erro

    def _salvar(self) -> None:
        conteudo = {
            "versao": _VERSAO_FORMATO,
            "proximo_id": self._proximo_id,
            "restaurantes": self._restaurantes,
        }
        temporario = self._caminho.with_name(self._caminho.name + ".tmp")

        try:
            self._caminho.parent.mkdir(parents=True, exist_ok=True)
            with temporario.open("wb") as arquivo:
                pickle.dump(conteudo, arquivo, protocol=pickle.HIGHEST_PROTOCOL)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self._caminho)
        except OSError as erro:
            self._remover_temporario(temporario)
            raise ErroPersistencia(
                f"nao foi possivel gravar o arquivo '{self._caminho}': {erro}"
            ) from erro
        except (pickle.PicklingError, TypeError, AttributeError) as erro:
            self._remover_temporario(temporario)
            raise ErroPersistencia(
                f"nao foi possivel serializar os restaurantes: {erro}"
            ) from erro

    @staticmethod
    def _remover_temporario(temporario: Path) -> None:
        try:
            temporario.unlink()
        except OSError:
            pass
