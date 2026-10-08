import os
import pickle
from pathlib import Path
from typing import Union

from source.dominio.usuarios.excecoes import ErroPersistencia
from source.dominio.usuarios.usuario import Usuario
from source.infraestrutura.persistencia.memoria import RepositorioUsuariosMemoria

_VERSAO_FORMATO = 1


class RepositorioUsuariosArquivo(RepositorioUsuariosMemoria):
    """Repositorio que persiste os usuarios em um arquivo binario (pickle).

    Reaproveita as consultas do repositorio em memoria: ao iniciar, carrega o
    arquivo para a RAM; a cada novo usuario, regrava o arquivo. Se a gravacao
    falhar, o estado em memoria e revertido e ErroPersistencia e levantada.

    Atencao: pickle nao e seguro contra arquivos maliciosos. Use apenas
    arquivos gerados pela propria aplicacao.
    """

    def __init__(self, caminho: Union[str, Path]) -> None:
        super().__init__()
        self._caminho = Path(caminho)
        self._carregar()

    def adicionar(self, usuario: Usuario) -> Usuario:
        proximo_id_anterior = self._proximo_id
        super().adicionar(usuario)
        try:
            self._salvar()
        except ErroPersistencia:
            # Reverte a RAM para que ela nao fique diferente do arquivo.
            self._usuarios.pop()
            self._proximo_id = proximo_id_anterior
            usuario.id = None
            raise
        return usuario

    def _carregar(self) -> None:
        if not self._caminho.exists():
            return

        try:
            with open(self._caminho, "rb") as arquivo:
                conteudo = pickle.load(arquivo)

            if (
                not isinstance(conteudo, dict)
                or conteudo.get("versao") != _VERSAO_FORMATO
                or not isinstance(conteudo.get("usuarios"), list)
                or not all(isinstance(u, Usuario) for u in conteudo["usuarios"])
            ):
                raise ValueError("estrutura do arquivo nao reconhecida")

            self._usuarios = conteudo["usuarios"]
            self._proximo_id = int(conteudo["proximo_id"])
        except IOError as erro:  # IOError e alias de OSError (arquivo/permissao/disco)
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
            "usuarios": self._usuarios,
        }
        temporario = self._caminho.with_name(self._caminho.name + ".tmp")

        try:
            self._caminho.parent.mkdir(parents=True, exist_ok=True)
            # Grava em arquivo temporario e troca no final: se algo falhar no
            # meio, o arquivo original continua integro.
            with open(temporario, "wb") as arquivo:
                pickle.dump(conteudo, arquivo, protocol=pickle.HIGHEST_PROTOCOL)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self._caminho)
        except IOError as erro:  # IOError e alias de OSError
            self._remover_temporario(temporario)
            raise ErroPersistencia(
                f"nao foi possivel gravar o arquivo '{self._caminho}': {erro}"
            ) from erro
        except (pickle.PicklingError, TypeError, AttributeError) as erro:
            self._remover_temporario(temporario)
            raise ErroPersistencia(
                f"nao foi possivel serializar os usuarios: {erro}"
            ) from erro

    @staticmethod
    def _remover_temporario(temporario: Path) -> None:
        try:
            temporario.unlink()
        except IOError:
            pass