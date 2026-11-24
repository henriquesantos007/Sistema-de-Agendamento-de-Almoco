import string
from typing import List, Optional

from source.dominio.usuarios.excecoes import LoginInvalido, SenhaInvalida

# Regras de login (Laboratorio 2)
LOGIN_TAMANHO_MAXIMO = 12

# Regras de senha: politica de senha padrao do AWS IAM
# https://docs.aws.amazon.com/pt_br/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html
SENHA_TAMANHO_MINIMO = 8
SENHA_TAMANHO_MAXIMO = 128
SENHA_TIPOS_MINIMOS = 3
CARACTERES_ESPECIAIS = "!@#$%^&*()_+-=[]{}|'"


def validar_login(login: Optional[str]) -> str:
    """Valida o login e devolve o valor normalizado (sem espacos nas pontas).

    Levanta LoginInvalido com todos os motivos encontrados.
    """
    login = (login or "").strip()
    motivos = []

    if not login:
        motivos.append("login e obrigatorio")
    else:
        if len(login) > LOGIN_TAMANHO_MAXIMO:
            motivos.append(
                f"login deve ter no maximo {LOGIN_TAMANHO_MAXIMO} caracteres"
            )
        if any(caractere.isdigit() for caractere in login):
            motivos.append("login nao pode conter numeros")

    if motivos:
        raise LoginInvalido(motivos)

    return login


def validar_senha(
    senha: Optional[str],
    login: Optional[str] = None,
    email: Optional[str] = None,
) -> None:
    """Valida a senha conforme a politica padrao do AWS IAM.

    Levanta SenhaInvalida com todos os motivos encontrados.
    """
    senha = senha or ""
    motivos = (
        _motivos_de_tamanho(senha)
        + _motivos_de_complexidade(senha)
        + _motivos_de_igualdade(senha, login, email)
    )
    if motivos:
        raise SenhaInvalida(motivos)


def _motivos_de_tamanho(senha: str) -> List[str]:
    motivos = []
    if len(senha) < SENHA_TAMANHO_MINIMO:
        motivos.append(
            f"senha deve ter no minimo {SENHA_TAMANHO_MINIMO} caracteres"
        )
    if len(senha) > SENHA_TAMANHO_MAXIMO:
        motivos.append(
            f"senha deve ter no maximo {SENHA_TAMANHO_MAXIMO} caracteres"
        )
    return motivos


def _motivos_de_complexidade(senha: str) -> List[str]:
    tipos_presentes = sum(
        (
            any(c in string.ascii_uppercase for c in senha),
            any(c in string.ascii_lowercase for c in senha),
            any(c in string.digits for c in senha),
            any(c in CARACTERES_ESPECIAIS for c in senha),
        )
    )
    if tipos_presentes >= SENHA_TIPOS_MINIMOS:
        return []
    return [
        f"senha deve conter ao menos {SENHA_TIPOS_MINIMOS} dos 4 tipos de "
        "caracteres: maiusculas, minusculas, numeros e especiais "
        f"({' '.join(CARACTERES_ESPECIAIS)})"
    ]


def _motivos_de_igualdade(
    senha: str, login: Optional[str], email: Optional[str]
) -> List[str]:
    motivos = []
    login_normalizado = (login or "").strip()
    if login_normalizado and senha == login_normalizado:
        motivos.append("senha nao pode ser identica ao login")

    email_normalizado = (email or "").strip()
    if email_normalizado and senha == email_normalizado:
        motivos.append("senha nao pode ser identica ao e-mail")
    return motivos