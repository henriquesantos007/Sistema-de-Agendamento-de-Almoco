from source.dominio.excecoes import ErroPersistenciaBase


class ErroPersistencia(ErroPersistenciaBase):
    """Falha ao carregar ou persistir restaurantes."""
