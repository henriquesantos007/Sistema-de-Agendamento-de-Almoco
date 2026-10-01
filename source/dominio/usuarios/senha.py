import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACOES = 600_000


def gerar_hash_senha(senha: str) -> str:
    sal = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), bytes.fromhex(sal), ITERACOES
    )
    return f"{ALGORITMO}${ITERACOES}${sal}${digest.hex()}"


def verificar_senha(senha: str, hash_senha: str) -> bool:
    try:
        algoritmo, iteracoes, sal, digest = hash_senha.split("$")
    except ValueError:
        return False
    if algoritmo != ALGORITMO:
        return False
    calculado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), bytes.fromhex(sal), int(iteracoes)
    )
    return hmac.compare_digest(calculado.hex(), digest)
