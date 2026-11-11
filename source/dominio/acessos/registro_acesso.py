from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class RegistroAcesso:
    """Um acesso de um usuario em um instante.

    Guarda so o identificador do usuario: login e perfil sao consultados no
    cadastro quando o relatorio e gerado. O instante e mantido em UTC.
    """

    usuario_id: int
    instante: datetime

    def __post_init__(self) -> None:
        if type(self.usuario_id) is not int or self.usuario_id < 1:
            raise ValueError(
                f"identificador de usuario invalido: {self.usuario_id!r}"
            )
        if not isinstance(self.instante, datetime):
            raise ValueError(f"instante invalido: {self.instante!r}")
        if self.instante.utcoffset() is None:
            raise ValueError("o instante do acesso precisa informar o fuso horario")

        object.__setattr__(
            self, "instante", self.instante.astimezone(timezone.utc)
        )
