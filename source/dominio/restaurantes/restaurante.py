from datetime import datetime, time
from enum import Enum
from typing import Optional

from source.dominio.restaurantes.dados_restaurante import DadosRestaurante


class StatusRestaurante(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    PENDENTE = "PENDENTE"


class Restaurante:
    def __init__(self, dados: DadosRestaurante) -> None:
        self.id: Optional[int] = None
        self.nome: str
        self.descricao: str
        self.localizacao: str
        self.telefone: str
        self.horario_limite_agendamento: time
        self.status: StatusRestaurante
        self.data_cadastro: datetime
        self._aplicar_dados(dados)
        self.status = StatusRestaurante.ATIVO
        self.data_cadastro = datetime.now()

    def atualizar_dados(self, dados: DadosRestaurante) -> None:
        self._aplicar_dados(dados)

    def _aplicar_dados(self, dados: DadosRestaurante) -> None:
        self.nome = dados.nome
        self.descricao = dados.descricao
        self.localizacao = dados.localizacao
        self.telefone = dados.telefone
        self.horario_limite_agendamento = dados.horario_limite_agendamento
