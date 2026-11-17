import copy

class UsuarioMemento:
    """Repositório opaco que guarda o snapshot do estado do Usuário."""
    def __init__(self, estado: dict):
        # Usamos deepcopy para garantir que o estado salvo não sofra mutações
        self._estado = copy.deepcopy(estado)

    def get_estado(self) -> dict:
        return copy.deepcopy(self._estado)