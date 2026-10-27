from datetime import time
from typing import List

from source.dominio.restaurantes import DadosRestaurante


class ValidadorRestaurante:
    def validar(self, dados: DadosRestaurante) -> List[str]:
        erros = []

        campos_obrigatorios = {
            "nome": dados.nome,
            "localizacao": dados.localizacao,
            "telefone": dados.telefone,
        }

        for campo, valor in campos_obrigatorios.items():
            if not isinstance(valor, str) or not valor.strip():
                erros.append(f"{campo} e obrigatorio")

        if not isinstance(dados.descricao, str):
            erros.append("descricao invalida")

        if not isinstance(dados.horario_limite_agendamento, time):
            erros.append("horario limite de agendamento invalido")

        return erros
