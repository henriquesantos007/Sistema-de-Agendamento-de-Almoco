import re


def normalizar_telefone(telefone: str) -> str:
    return re.sub(r"\D", "", telefone)
