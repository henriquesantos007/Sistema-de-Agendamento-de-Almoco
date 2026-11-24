import copy
from typing import Any, Dict, Optional, Type


class UsuarioMemento:
    """Snapshot protegido por cópias profundas e associado à entidade de origem."""

    def __init__(
        self,
        estado: Dict[str, Any],
        tipo_origem: Type[object],
        id_origem: Optional[int],
    ) -> None:
        self._estado = copy.deepcopy(estado)
        self._tipo_origem = tipo_origem
        self._id_origem = id_origem

    def _estado_para(
        self,
        tipo_destino: Type[object],
        id_destino: Optional[int],
    ) -> Dict[str, Any]:
        if tipo_destino is not self._tipo_origem or id_destino != self._id_origem:
            raise ValueError("O memento não pertence a esta entidade.")
        return copy.deepcopy(self._estado)