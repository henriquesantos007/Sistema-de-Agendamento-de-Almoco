import re
from typing import List

from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios


class DadosUsuarioInvalidos(ValueError):
    def __init__(self, erros: List[str]) -> None:
        self.erros = erros
        super().__init__("; ".join(erros))


class ValidadorUsuario:
    PERFIS_VALIDOS = {"estudante", "gestor_restaurante", "administrador"}
    FORMATO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, repositorio: RepositorioUsuarios) -> None:
        self.repositorio = repositorio

    def validar(self, dados: DadosUsuario) -> List[str]:
        erros = []
        campos_obrigatorios = {
            "nome": dados.nome,
            "email": dados.email,
            "senha": dados.senha,
            "telefone": dados.telefone,
        }
        for campo, valor in campos_obrigatorios.items():
            if not valor or not valor.strip():
                erros.append(f"{campo} e obrigatorio")

        perfil = dados.perfil.strip().lower()
        if perfil not in self.PERFIS_VALIDOS:
            erros.append("perfil invalido")

        if dados.email and not self.FORMATO_EMAIL.match(dados.email.strip()):
            erros.append("e-mail invalido")
        elif dados.email and self.repositorio.buscar_por_email(dados.email):
            erros.append("e-mail ja cadastrado")

        if perfil == "estudante":
            if not dados.matricula or not dados.matricula.strip():
                erros.append("matricula e obrigatoria para estudante")
            elif self.repositorio.existe_matricula(dados.matricula):
                erros.append("matricula ja cadastrada")

            if dados.telefone and self.repositorio.existe_telefone(dados.telefone):
                erros.append("telefone ja cadastrado para estudante")

        if perfil == "gestor_restaurante" and dados.restaurante_id is None:
            erros.append("restaurante e obrigatorio para gestor")

        return erros