from datetime import datetime, time
from enum import Enum
from typing import Optional


class StatusRestaurante(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    PENDENTE = "PENDENTE"


class Restaurante:
    def __init__(
        self,
        nome: str,
        localizacao: str,
        telefone: str,
        horario_limite_agendamento: time,
        descricao: str = "",
        id: Optional[int] = None,
        data_cadastro: Optional[datetime] = None,
        status: StatusRestaurante = StatusRestaurante.ATIVO,
    ) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.localizacao = localizacao
        self.telefone = telefone
        self.horario_limite_agendamento = horario_limite_agendamento
        self.status = status
        self.data_cadastro = data_cadastro or datetime.now()

    def atualizar_dados(
        self,
        nome: str,
        descricao: str,
        localizacao: str,
        telefone: str,
        horario_limite_agendamento: time,
    ) -> None:
        self.nome = nome
        self.descricao = descricao
        self.localizacao = localizacao
        self.telefone = telefone
        self.horario_limite_agendamento = horario_limite_agendamento
