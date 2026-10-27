from typing import List


class DadosRestauranteInvalidos(ValueError):
    def __init__(self, erros: List[str]) -> None:
        self.erros = erros
        super().__init__("; ".join(erros))


class RestauranteNaoEncontrado(LookupError):
    def __init__(self, restaurante_id: int) -> None:
        self.restaurante_id = restaurante_id
        super().__init__(f"restaurante nao encontrado: {restaurante_id}")


class RestauranteVinculado(ValueError):
    def __init__(self, restaurante_id: int) -> None:
        self.restaurante_id = restaurante_id
        super().__init__(
            f"restaurante {restaurante_id} possui gestores vinculados"
        )
