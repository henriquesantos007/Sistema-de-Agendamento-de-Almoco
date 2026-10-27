from typing import List, Optional

from source.dominio.restaurantes import Restaurante, RepositorioRestaurantes


class RepositorioRestaurantesMemoria(RepositorioRestaurantes):
    def __init__(self) -> None:
        self._restaurantes: List[Restaurante] = []
        self._proximo_id = 1

    def adicionar(self, restaurante: Restaurante) -> Restaurante:
        if any(cadastrado is restaurante for cadastrado in self._restaurantes):
            raise ValueError("restaurante ja cadastrado")

        restaurante.id = self._proximo_id
        self._proximo_id += 1
        self._restaurantes.append(restaurante)
        return restaurante

    def buscar_por_id(self, restaurante_id: int) -> Optional[Restaurante]:
        return next(
            (
                restaurante
                for restaurante in self._restaurantes
                if restaurante.id == restaurante_id
            ),
            None,
        )

    def listar_todos(self) -> List[Restaurante]:
        return list(self._restaurantes)

    def atualizar(self, restaurante: Restaurante) -> Restaurante:
        if restaurante.id is None:
            raise ValueError("restaurante precisa de identificador para atualizacao")

        for indice, existente in enumerate(self._restaurantes):
            if existente.id == restaurante.id:
                self._restaurantes[indice] = restaurante
                return restaurante

        raise ValueError(f"restaurante nao encontrado: {restaurante.id}")

    def remover(self, restaurante_id: int) -> bool:
        for indice, restaurante in enumerate(self._restaurantes):
            if restaurante.id == restaurante_id:
                del self._restaurantes[indice]
                return True

        return False

    def contar(self) -> int:
        return len(self._restaurantes)
