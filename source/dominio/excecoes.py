class ErroPersistenciaBase(Exception):
    """Base comum das falhas de persistencia de qualquer entidade.

    Cada dominio mantem sua propria ErroPersistencia; herdar desta base permite
    que os clientes capturem todas com um unico except.
    """
