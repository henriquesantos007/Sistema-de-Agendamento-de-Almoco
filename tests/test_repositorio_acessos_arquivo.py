import json
from datetime import datetime, timedelta, timezone

import pytest

from source.dominio.acessos import (
    ErroPersistencia,
    RegistroAcesso,
    RepositorioAcessos,
)
from source.dominio.excecoes import ErroPersistenciaBase
from source.infraestrutura.persistencia.arquivo import RepositorioAcessosArquivo
from source.infraestrutura.persistencia.memoria import RepositorioAcessosMemoria


def registro(usuario_id, minuto=0):
    return RegistroAcesso(
        usuario_id=usuario_id,
        instante=datetime(2026, 11, 10, 15, minuto, 56, tzinfo=timezone.utc),
    )


@pytest.fixture
def caminho(tmp_path):
    return tmp_path / "dados" / "acessos.jsonl"


def test_deve_implementar_o_contrato_sem_herdar_da_versao_em_memoria(caminho):
    repositorio = RepositorioAcessosArquivo(caminho)

    assert isinstance(repositorio, RepositorioAcessos)
    assert not isinstance(repositorio, RepositorioAcessosMemoria)


def test_arquivo_inexistente_nao_deve_ter_registros(caminho):
    assert RepositorioAcessosArquivo(caminho).listar_todos() == []
    assert not caminho.exists()


def test_deve_gravar_uma_linha_json_por_registro_com_instante_em_utc(caminho):
    repositorio = RepositorioAcessosArquivo(caminho)
    fuso_local = timezone(timedelta(hours=-3))

    repositorio.registrar(
        RegistroAcesso(
            usuario_id=3,
            instante=datetime(2026, 11, 10, 12, 34, 56, tzinfo=fuso_local),
        )
    )

    linhas = caminho.read_text(encoding="utf-8").splitlines()
    assert [json.loads(linha) for linha in linhas] == [
        {"usuario_id": 3, "instante": "2026-11-10T15:34:56+00:00"}
    ]


def test_deve_acrescentar_sem_reescrever_as_linhas_anteriores(caminho):
    repositorio = RepositorioAcessosArquivo(caminho)
    repositorio.registrar(registro(1, 1))
    conteudo_anterior = caminho.read_bytes()

    repositorio.registrar(registro(2, 2))

    conteudo = caminho.read_bytes()
    assert conteudo.startswith(conteudo_anterior)
    assert len(conteudo.splitlines()) == 2


def test_registros_devem_sobreviver_a_uma_nova_instancia(caminho):
    registros = [registro(2, 5), registro(1, 1), registro(2, 3)]
    primeiro = RepositorioAcessosArquivo(caminho)
    for item in registros:
        primeiro.registrar(item)

    assert RepositorioAcessosArquivo(caminho).listar_todos() == registros


@pytest.mark.parametrize(
    "linha",
    [
        "isto nao e json",
        "[1, 2]",
        '{"usuario_id": 3}',
        '{"usuario_id": "3", "instante": "2026-11-10T15:34:56+00:00"}',
        '{"usuario_id": 0, "instante": "2026-11-10T15:34:56+00:00"}',
        '{"usuario_id": 3, "instante": "ontem"}',
        '{"usuario_id": 3, "instante": "2026-11-10T15:34:56"}',
        '{"usuario_id": 3, "instante": 1}',
        "",
    ],
)
def test_linha_invalida_deve_virar_erro_de_persistencia(caminho, linha):
    repositorio = RepositorioAcessosArquivo(caminho)
    repositorio.registrar(registro(1))
    with caminho.open("a", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(linha + "\n")

    with pytest.raises(ErroPersistencia, match="linha 2"):
        repositorio.listar_todos()


def test_falha_de_gravacao_deve_virar_erro_de_persistencia(tmp_path):
    ocupado = tmp_path / "ocupado"
    ocupado.write_text("nao e um diretorio", encoding="utf-8")
    repositorio = RepositorioAcessosArquivo(ocupado / "acessos.jsonl")

    with pytest.raises(ErroPersistencia, match="gravar") as excecao:
        repositorio.registrar(registro(1))

    assert isinstance(excecao.value.__cause__, OSError)


def test_falha_de_leitura_deve_virar_erro_de_persistencia(tmp_path):
    diretorio = tmp_path / "acessos.jsonl"
    diretorio.mkdir()

    with pytest.raises(ErroPersistencia, match="ler"):
        RepositorioAcessosArquivo(diretorio).listar_todos()


def test_erro_de_persistencia_deve_herdar_da_base_comum():
    assert issubclass(ErroPersistencia, ErroPersistenciaBase)


def test_gravacoes_concorrentes_nao_devem_perder_registros(caminho):
    import threading

    repositorio = RepositorioAcessosArquivo(caminho)
    threads_total, registros_por_thread = 8, 25

    def gravar(usuario_id):
        for _ in range(registros_por_thread):
            repositorio.registrar(registro(usuario_id))

    threads = [
        threading.Thread(target=gravar, args=(indice + 1,))
        for indice in range(threads_total)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(repositorio.listar_todos()) == threads_total * registros_por_thread


def test_acrescimo_apos_linha_final_sem_quebra_deve_iniciar_nova_linha(caminho):
    caminho.parent.mkdir(parents=True)
    caminho.write_bytes(
        b'{"usuario_id": 1, "instante": "2026-11-10T15:00:56+00:00"}'
    )
    repositorio = RepositorioAcessosArquivo(caminho)

    repositorio.registrar(registro(2, 1))

    assert repositorio.listar_todos() == [registro(1, 0), registro(2, 1)]


def test_acrescimo_nao_deve_colar_registro_em_linha_truncada(caminho):
    caminho.parent.mkdir(parents=True)
    caminho.write_bytes(b'{"usuario_id": 2, "inst')
    repositorio = RepositorioAcessosArquivo(caminho)

    repositorio.registrar(registro(3))

    linhas = caminho.read_text(encoding="utf-8").splitlines()
    assert linhas[0] == '{"usuario_id": 2, "inst'
    assert json.loads(linhas[1])["usuario_id"] == 3


@pytest.mark.parametrize(
    "linha",
    [
        '{"usuario_id": 1, "instante": "0001-01-01T00:00:00+05:00"}',
        '{"usuario_id": 1, "instante": ' + "[" * 100000 + "]" * 100000 + "}",
    ],
    ids=["instante_fora_do_intervalo", "json_aninhado_demais"],
)
def test_linha_fora_dos_limites_deve_virar_erro_de_persistencia(caminho, linha):
    caminho.parent.mkdir(parents=True)
    caminho.write_text(linha + "\n", encoding="utf-8")

    with pytest.raises(ErroPersistencia, match="linha 1"):
        RepositorioAcessosArquivo(caminho).listar_todos()
