from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DadosUsuario:
    perfil: str
    nome: str
    login: str
    email: str
    senha: str
    telefone: str
    matricula: Optional[str] = None
    restaurante_id: Optional[int] = None