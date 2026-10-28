from typing import List

from source.aplicacao.restaurantes.excecoes import (
    DadosRestauranteInvalidos,
    RestauranteNaoEncontrado,
    RestauranteVinculado,
)
from source.aplicacao.restaurantes.validador_restaurante import (
    ValidadorRestaurante,
)
from source.dominio.restaurantes import (
    DadosRestaurante,
    Restaurante,
    RepositorioRestaurantes,
)
from source.dominio.usuarios import GestorRestaurante, RepositorioUsuarios


class ControladorRestaurante:
    def __init__(
        self,
        repositorio: RepositorioRestaurantes,
        validador: ValidadorRestaurante,
        repositorio_usuarios: RepositorioUsuarios,
    ) -> None:
        self.repositorio = repositorio
        self.validador = validador
        self.repositorio_usuarios = repositorio_usuarios

    def cadastrar(self, dados: DadosRestaurante) -> Restaurante:
        dados_validos = self._validar_e_normalizar(dados)
        restaurante = Restaurante(dados_validos)
        return self.repositorio.adicionar(restaurante)

    def buscar_por_id(self, restaurante_id: int) -> Restaurante:
        restaurante = self.repositorio.buscar_por_id(restaurante_id)
        if restaurante is None:
            raise RestauranteNaoEncontrado(restaurante_id)
        return restaurante

    def listar_todos(self) -> List[Restaurante]:
        return self.repositorio.listar_todos()

    def contar(self) -> int:
        return self.repositorio.contar()

    def atualizar(
        self,
        restaurante_id: int,
        dados: DadosRestaurante,
    ) -> Restaurante:
        restaurante = self.buscar_por_id(restaurante_id)
        dados_validos = self._validar_e_normalizar(dados)
        restaurante.atualizar_dados(dados_validos)
        return self.repositorio.atualizar(restaurante)

    def remover(self, restaurante_id: int) -> bool:
        if self.repositorio.buscar_por_id(restaurante_id) is None:
            return False

        gestores_vinculados = any(
            isinstance(usuario, GestorRestaurante)
            and usuario.restaurante_id == restaurante_id
            for usuario in self.repositorio_usuarios.listar_todos()
        )
        if gestores_vinculados:
            raise RestauranteVinculado(restaurante_id)

        return self.repositorio.remover(restaurante_id)

    def _validar_e_normalizar(self, dados: DadosRestaurante) -> DadosRestaurante:
        erros = self.validador.validar(dados)
        if erros:
            raise DadosRestauranteInvalidos(erros)

        return DadosRestaurante(
            nome=dados.nome.strip(),
            descricao=dados.descricao.strip(),
            localizacao=dados.localizacao.strip(),
            telefone=dados.telefone.strip(),
            horario_limite_agendamento=dados.horario_limite_agendamento,
        )
