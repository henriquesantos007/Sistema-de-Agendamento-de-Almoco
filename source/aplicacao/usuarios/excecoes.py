from typing import List

class DadosUsuarioInvalidos(ValueError):
    def __init__(self, erros: List[str]) -> None:
        self.erros = erros
        super().__init__("; ".join(erros))