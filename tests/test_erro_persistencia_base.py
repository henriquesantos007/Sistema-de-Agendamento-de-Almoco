import pytest

from source.dominio.excecoes import ErroPersistenciaBase
from source.dominio.restaurantes import ErroPersistencia as ErroPersistenciaRestaurantes
from source.dominio.usuarios import ErroPersistencia as ErroPersistenciaUsuarios


@pytest.mark.parametrize(
    "erro", [ErroPersistenciaUsuarios, ErroPersistenciaRestaurantes]
)
def test_erros_de_persistencia_devem_herdar_da_base_comum(erro):
    with pytest.raises(ErroPersistenciaBase):
        raise erro("falha")
