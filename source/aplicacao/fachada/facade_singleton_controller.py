import threading
from typing import Dict, List, Optional

from source.aplicacao.logger_aplicacao import LoggerAplicacao
from source.aplicacao.relatorios import Documento, ServicoRelatorioAcesso
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
from source.dominio.acessos import RepositorioAcessos
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

    # copy/deepcopy chamariam o __new__ acima; a cópia de um Singleton é ele mesmo.
    def __copy__(self) -> "FacadeSingletonController":
        return self

    def __deepcopy__(self, memo: dict) -> "FacadeSingletonController":
        return self

    @classmethod
    def obter_instancia(
        cls,
        repositorio_usuarios: Optional[RepositorioUsuarios] = None,
        repositorio_restaurantes: Optional[RepositorioRestaurantes] = None,
        repositorio_acessos: Optional[RepositorioAcessos] = None,
        logger: Optional[LoggerAplicacao] = None,
    ) -> "FacadeSingletonController":
        # Copia local: um reiniciar() concorrente não pode zerar a instância
        # entre a validação e o retorno.
        instancia = cls._instancia
        if instancia is None:
            with cls._trava:
                if cls._instancia is None:
                    cls._instancia = cls._criar(
                        repositorio_usuarios,
                        repositorio_restaurantes,
                        repositorio_acessos,
                        logger,
                    )
                    return cls._instancia
                instancia = cls._instancia

        instancia._validar_repositorios_inalterados(
            repositorio_usuarios,
            repositorio_restaurantes,
            repositorio_acessos,
            logger,
        )
        return instancia

    def _validar_repositorios_inalterados(
        self,
        repositorio_usuarios: Optional[RepositorioUsuarios],
        repositorio_restaurantes: Optional[RepositorioRestaurantes],
        repositorio_acessos: Optional[RepositorioAcessos] = None,
        logger: Optional[LoggerAplicacao] = None,
    ) -> None:
        pares = (
            (repositorio_usuarios, self._repositorio_usuarios),
            (repositorio_restaurantes, self._repositorio_restaurantes),
            (repositorio_acessos, self._repositorio_acessos),
            (logger, self._logger),
        )

        if any(
            informado is not None and informado is not atual
            for informado, atual in pares
        ):
            raise ValueError(
                "A fachada já foi inicializada com outros repositórios "
                "ou outro logger."
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
        repositorio_acessos: Optional[RepositorioAcessos],
        logger: Optional[LoggerAplicacao],
    ) -> "FacadeSingletonController":
        dependencias = (
            repositorio_usuarios,
            repositorio_restaurantes,
            repositorio_acessos,
            logger,
        )
        if any(dependencia is None for dependencia in dependencias):
            raise ValueError(
                "A primeira chamada de obter_instancia exige os repositórios "
                "de usuários, de restaurantes e de acessos e o logger."
            )

        instancia = object.__new__(cls)
        instancia._repositorio_usuarios = repositorio_usuarios
        instancia._repositorio_restaurantes = repositorio_restaurantes
        instancia._repositorio_acessos = repositorio_acessos
        instancia._logger = logger
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
        instancia._servico_relatorio_acesso = ServicoRelatorioAcesso(
            repositorio_acessos,
            repositorio_usuarios,
            logger,
        )
        return instancia

    def cadastrar_usuario(self, dados: DadosUsuario) -> Usuario:
        return self._controlador_usuario.cadastrar(dados)

    def listar_usuarios(self) -> List[Usuario]:
        return self._controlador_usuario.listar_todos()

    def buscar_usuario(self, usuario_id: int) -> Usuario:
        return self._controlador_usuario.buscar_por_id(usuario_id)

    def atualizar_usuario(
        self,
        usuario_id: int,
        dados: DadosUsuario,
    ) -> Usuario:
        return self._controlador_usuario.atualizar(usuario_id, dados)

    def remover_usuario(self, usuario_id: int) -> None:
        self._controlador_usuario.remover(usuario_id)

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
        # Registros de acesso sao eventos, nao entidades cadastradas (RF12).
        return {
            self.CHAVE_USUARIOS: self.contar_usuarios(),
            self.CHAVE_RESTAURANTES: self.contar_restaurantes(),
        }

    def contar_total_entidades(self) -> int:
        return sum(self.obter_contagem_por_entidade().values())

    def gerar_relatorio_acessos(self, formato: str) -> Documento:
        return self._servico_relatorio_acesso.gerar(formato)