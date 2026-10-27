import threading
from typing import Dict, List, Optional

from source.aplicacao.restaurantes import (
    ControladorRestaurante,
    ValidadorRestaurante,
)
from source.aplicacao.usuarios import ControladorUsuario, DadosUsuario
from source.aplicacao.usuarios.validador_usuario import (
    ValidadorDadosObrigatorios,
    ValidadorEmail,
    ValidadorEstudante,
    ValidadorGestorRestaurante,
    ValidadorLogin,
    ValidadorPerfil,
    ValidadorSenha,
    ValidadorUsuario,
)
from source.dominio.restaurantes import (
    DadosRestaurante,
    RepositorioRestaurantes,
    Restaurante,
)
from source.dominio.usuarios import RepositorioUsuarios, Usuario


class FacadeSingletonController:
    CHAVE_USUARIOS = "usuarios"
    CHAVE_RESTAURANTES = "restaurantes"

    _instancia: Optional["FacadeSingletonController"] = None
    _trava = threading.Lock()

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            "Use FacadeSingletonController.obter_instancia(...) "
            "em vez de instanciar diretamente."
        )

    @classmethod
    def obter_instancia(
        cls,
        repositorio_usuarios: Optional[RepositorioUsuarios] = None,
        repositorio_restaurantes: Optional[RepositorioRestaurantes] = None,
    ) -> "FacadeSingletonController":
        if cls._instancia is None:
            with cls._trava:
                if cls._instancia is None:
                    cls._instancia = cls._criar(
                        repositorio_usuarios, repositorio_restaurantes
                    )
                    return cls._instancia

        cls._validar_repositorios_inalterados(repositorio_usuarios, repositorio_restaurantes)
        return cls._instancia

    @classmethod
    def _validar_repositorios_inalterados(
        cls,
        repositorio_usuarios: Optional[RepositorioUsuarios],
        repositorio_restaurantes: Optional[RepositorioRestaurantes],
    ) -> None:
        instancia = cls._instancia
        usuarios_alterados = (
            repositorio_usuarios is not None
            and repositorio_usuarios is not instancia._repositorio_usuarios
        )
        restaurantes_alterados = (
            repositorio_restaurantes is not None
            and repositorio_restaurantes is not instancia._repositorio_restaurantes
        )
        
        if usuarios_alterados or restaurantes_alterados:
            raise ValueError(
                "A fachada já foi inicializada com outros repositórios."
            )

    @classmethod
    def reiniciar(cls) -> None:
        """Descarta a instância atual. Use em testes ou ao trocar o armazenamento."""
        with cls._trava:
            cls._instancia = None

    @classmethod
    def _criar(
        cls,
        repositorio_usuarios: Optional[RepositorioUsuarios],
        repositorio_restaurantes: Optional[RepositorioRestaurantes],
    ) -> "FacadeSingletonController":
        if repositorio_usuarios is None or repositorio_restaurantes is None:
            raise ValueError(
                "A primeira chamada de obter_instancia exige os repositórios "
                "de usuários e de restaurantes."
            )

        instancia = object.__new__(cls)
        instancia._repositorio_usuarios = repositorio_usuarios
        instancia._repositorio_restaurantes = repositorio_restaurantes
        instancia._controlador_usuario = ControladorUsuario(
            repositorio_usuarios,
            ValidadorUsuario([
                ValidadorDadosObrigatorios(),
                ValidadorPerfil(),
                ValidadorLogin(),
                ValidadorEmail(),
                ValidadorSenha(),
                ValidadorEstudante(),
                ValidadorGestorRestaurante(repositorio_restaurantes),
            ]),
        )
        instancia._controlador_restaurante = ControladorRestaurante(
            repositorio_restaurantes,
            ValidadorRestaurante(),
            repositorio_usuarios,
        )
        return instancia

    def cadastrar_usuario(self, dados: DadosUsuario) -> Usuario:
        return self._controlador_usuario.cadastrar(dados)

    def listar_usuarios(self) -> List[Usuario]:
        return self._controlador_usuario.listar_todos()

    def cadastrar_restaurante(self, dados: DadosRestaurante) -> Restaurante:
        return self._controlador_restaurante.cadastrar(dados)

    def buscar_restaurante(self, restaurante_id: int) -> Restaurante:
        return self._controlador_restaurante.buscar_por_id(restaurante_id)

    def listar_restaurantes(self) -> List[Restaurante]:
        return self._controlador_restaurante.listar_todos()

    def atualizar_restaurante(
        self,
        restaurante_id: int,
        dados: DadosRestaurante,
    ) -> Restaurante:
        return self._controlador_restaurante.atualizar(restaurante_id, dados)

    def remover_restaurante(self, restaurante_id: int) -> bool:
        return self._controlador_restaurante.remover(restaurante_id)

    def contar_usuarios(self) -> int:
        return self._controlador_usuario.contar()

    def contar_restaurantes(self) -> int:
        return self._controlador_restaurante.contar()

    def obter_contagem_por_entidade(self) -> Dict[str, int]:
        return {
            self.CHAVE_USUARIOS: self.contar_usuarios(),
            self.CHAVE_RESTAURANTES: self.contar_restaurantes(),
        }

    def contar_total_entidades(self) -> int:
        return sum(self.obter_contagem_por_entidade().values())