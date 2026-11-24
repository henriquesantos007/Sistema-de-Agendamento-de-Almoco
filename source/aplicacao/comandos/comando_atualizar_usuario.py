from typing import Optional

from source.aplicacao.comandos.comando import Comando
from source.aplicacao.usuarios.controlador_usuario import ControladorUsuario
from source.aplicacao.usuarios.dados_usuario import DadosUsuario
from source.dominio.usuarios.memento import UsuarioMemento
from source.dominio.usuarios.repositorio_usuarios import RepositorioUsuarios
from source.dominio.usuarios.usuario import Usuario


class ComandoAtualizarUsuario(Comando):
    """
    Comando Concreto que encapsula a atualização de um usuário.
    Atua como gerenciador temporário do Memento para a operação de desfazer.
    """

    def __init__(
        self,
        controlador: ControladorUsuario,
        repositorio: RepositorioUsuarios,
        id_usuario: int,
        dados_novos: DadosUsuario,
    ) -> None:
        self._controlador = controlador
        self._repositorio = repositorio
        self._id_usuario = id_usuario
        self._dados_novos = dados_novos
        self._memento: Optional[UsuarioMemento] = None
        self._usuario_alvo: Optional[Usuario] = None

    @property
    def usuario_id(self) -> int:
        return self._id_usuario

    def executar(self) -> Usuario:
        # Busca a entidade atual antes de aplicar as alterações
        self._usuario_alvo = self._repositorio.buscar_por_id(self._id_usuario)
        
        if not self._usuario_alvo:
            raise ValueError(f"Usuário com ID '{self._id_usuario}' não encontrado.")
            
        # Salva o snapshot (Memento) do estado original
        self._memento = self._usuario_alvo.criar_memento()
        
        # Delega a execução real para o Receptor (ControladorUsuario)
        # O controlador fará as validações de regra de negócio normalmente
        return self._controlador.atualizar(self._id_usuario, self._dados_novos)

    def desfazer(self) -> Usuario:
        if not self._memento or not self._usuario_alvo:
            raise ValueError("Não há estado anterior capturado para restaurar.")
            
        # Restaura o estado original na entidade que está em memória
        self._usuario_alvo.restaurar_memento(self._memento)
        
        # Força o repositório a persistir o estado revertido (Arquivo/Banco)
        return self._repositorio.atualizar(self._usuario_alvo)