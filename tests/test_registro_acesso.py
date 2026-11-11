from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from source.dominio.acessos import RegistroAcesso, RepositorioAcessos

INSTANTE = datetime(2026, 11, 10, 15, 34, 56, tzinfo=timezone.utc)


def test_deve_guardar_usuario_e_instante():
    registro = RegistroAcesso(usuario_id=3, instante=INSTANTE)

    assert registro.usuario_id == 3
    assert registro.instante == INSTANTE


def test_deve_converter_o_instante_para_utc():
    fuso_local = timezone(timedelta(hours=-3))
    registro = RegistroAcesso(
        usuario_id=3,
        instante=datetime(2026, 11, 10, 12, 34, 56, tzinfo=fuso_local),
    )

    assert registro.instante == INSTANTE
    assert registro.instante.utcoffset() == timedelta(0)


def test_deve_recusar_instante_sem_fuso_horario():
    with pytest.raises(ValueError, match="fuso"):
        RegistroAcesso(usuario_id=3, instante=datetime(2026, 11, 10, 12, 0))


@pytest.mark.parametrize("usuario_id", [0, -1, "3", 3.0, True, None])
def test_deve_recusar_identificador_de_usuario_invalido(usuario_id):
    with pytest.raises(ValueError, match="usuario"):
        RegistroAcesso(usuario_id=usuario_id, instante=INSTANTE)


def test_registro_deve_ser_imutavel():
    registro = RegistroAcesso(usuario_id=3, instante=INSTANTE)

    with pytest.raises(FrozenInstanceError):
        registro.usuario_id = 4


def test_contrato_deve_oferecer_apenas_registrar_e_listar():
    assert RepositorioAcessos.__abstractmethods__ == {"registrar", "listar_todos"}
    assert not hasattr(RepositorioAcessos, "atualizar")
    assert not hasattr(RepositorioAcessos, "remover")


def test_instante_fora_do_intervalo_em_utc_deve_ser_recusado():
    fuso = timezone(timedelta(hours=5))

    with pytest.raises(ValueError, match="instante"):
        RegistroAcesso(usuario_id=1, instante=datetime(1, 1, 1, tzinfo=fuso))
