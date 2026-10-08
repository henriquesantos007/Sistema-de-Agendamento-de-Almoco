from typing import List


class ErroValidacaoCampo(ValueError):
    """Base das excecoes de validacao de um campo do usuario.

    Guarda todos os motivos pelos quais o valor foi recusado, para que o
    chamador possa exibir todas as violacoes de uma so vez.
    """

    campo: str = ""

    def __init__(self, motivos: List[str]) -> None:
        self.motivos = list(motivos)
        super().__init__("; ".join(self.motivos))


class LoginInvalido(ErroValidacaoCampo):
    campo = "login"


class SenhaInvalida(ErroValidacaoCampo):
    campo = "senha"