from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class DadosRestaurante:
    nome: str
    localizacao: str
    telefone: str
    horario_limite_agendamento: time
    descricao: str = ""
