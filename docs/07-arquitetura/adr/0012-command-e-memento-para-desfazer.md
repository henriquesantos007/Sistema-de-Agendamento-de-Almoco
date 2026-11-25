# ADR-0012: Fachada baseada em Command para desfazer a atualização de usuário com Memento

- Status: Aceito
- Data: 2026-11-17

## Contexto

A Sprint 5 exige que o Administrador possa desfazer a última atualização bem-sucedida da entidade principal do sistema, `Usuario`, durante a execução atual. O sistema precisa capturar o estado da entidade imediatamente antes da alteração e, caso o Administrador solicite, restaurar e persistir esse estado. Fazer isso diretamente no controlador misturaria a lógica de regras de negócio com o controle de histórico e violaria o encapsulamento da entidade. A Sprint 5 também solicita a aplicação de padrões comportamentais (GoF) para resolver esse problema.

## Decisão

Implementar a reversão combinando os padrões comportamentais **Command** e **Memento**:

- **Memento no Domínio:** Em `source/dominio/usuarios/`, a entidade `Usuario` atua como *Originator* e `UsuarioMemento` guarda uma cópia profunda (`copy.deepcopy`) do estado, associada à classe concreta e ao identificador de origem. O atributo e o método de acesso são privados por convenção Python; o método devolve uma cópia profunda e a restauração rejeita tipo ou identificador diferentes.
- **Command na Aplicação:** Em `source/aplicacao/comandos/`, `Comando` é a interface abstrata e `ComandoAtualizarUsuario` é o Command concreto. Antes da atualização, o comando captura o memento e delega a operação validada ao `ControladorUsuario` (*Receiver*). Para desfazer, restaura o usuário e solicita ao repositório que persista o estado restaurado.
- **Papéis do Command e do Memento:** `Usuario` é o *Originator* e `UsuarioMemento` é o *Memento*. `ComandoAtualizarUsuario` atua como *Caretaker* do memento, mantendo o snapshot necessário ao desfazimento. `FacadeSingletonController` atua como *Invoker* e mantém somente a referência do último comando desfazível; após o sucesso, limpa essa referência.

## Consequências

- A entidade `Usuario` preserva seu encapsulamento, sendo a única que sabe como seu estado é extraído e injetado.
- O `ControladorUsuario` continua responsável apenas pelas regras de negócio e validações, respeitando o Princípio da Responsabilidade Única (SRP).
- O histórico contém somente a atualização de usuário concluída com sucesso mais recente e só pode ser consumido uma vez. Um histórico maior ou ações de outros tipos não fazem parte desta decisão.
- Somente `atualizar_usuario` usa Command nesta fachada; os demais casos de uso continuam delegando diretamente aos controladores.
- Se a persistência do desfazimento falhar, o repositório mantém o estado atualizado e a fachada conserva o comando para permitir nova tentativa.
- Se o usuário associado à atualização disponível é removido, a fachada descarta esse comando para evitar tentar restaurar uma entidade inexistente.
- O histórico em memória não é protegido por nova sincronização além da configuração existente da instância Singleton.
- Introduz uma leve camada extra de abstração na aplicação, visto que o fluxo agora passa pela criação e execução de um objeto de comando antes de chegar ao controlador.

## Alternativas consideradas

- Manter o histórico e uma cópia do estado diretamente no `ControladorUsuario`: rejeitada por ferir o encapsulamento da entidade (que teria seus atributos expostos) e por acoplar o gerenciamento de histórico na mesma classe que faz a validação de regras de negócio.
- Consultar o repositório de arquivo/banco de dados para resgatar o estado antigo: rejeitada porque os repositórios atuais gravam as alterações de forma atômica. Uma vez que o usuário foi atualizado, o arquivo binário antigo já foi sobrescrito pela escrita atômica (detalhada na ADR-0009).

## Relação com decisões anteriores

Esta decisão estende diretamente a **ADR-0008**, pois a `FacadeSingletonController` passa a instanciar o comando e manter a única referência desfazível. O `ComandoAtualizarUsuario` mantém o memento. Ao desfazer, o comando envia a entidade restaurada ao repositório selecionado segundo a **ADR-0009**, que persiste em memória ou em arquivo.