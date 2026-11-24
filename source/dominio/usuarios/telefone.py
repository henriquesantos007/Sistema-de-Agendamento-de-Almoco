import re


def normalizar_telefone(telefone: str) -> str:
    """Mantem apenas os digitos ASCII (0-9), de forma idempotente.

    Nao acrescenta ou remove codigo de pais, nao infere DDD e nao aplica
    regras de tamanho: apenas descarta caracteres que nao sao digitos ASCII.
    """
    return re.sub(r"[^0-9]", "", telefone)
