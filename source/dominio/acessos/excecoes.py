from source.dominio.excecoes import ErroPersistenciaBase


class ErroPersistencia(ErroPersistenciaBase):
    """Falha ao ler ou gravar registros de acesso."""
