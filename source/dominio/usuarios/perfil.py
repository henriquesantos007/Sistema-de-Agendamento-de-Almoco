from enum import Enum
from typing import Optional


class Perfil(Enum):
    ESTUDANTE = "estudante"
    GESTOR_RESTAURANTE = "gestor_restaurante"
    ADMINISTRADOR = "administrador"

    @classmethod
    def de_texto(cls, texto: Optional[str]) -> Optional["Perfil"]:
        valor = (texto or "").strip().lower()
        return next((perfil for perfil in cls if perfil.value == valor), None)
