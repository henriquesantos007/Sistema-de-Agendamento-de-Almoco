# ADR-0012: Reverter a última atualização de usuário com Command e Memento

- Status: Aceito
- Data: 2026-11-17

## Contexto

A Sprint 5 exige a implementação de uma funcionalidade para "desfazer a última atualização" de um usuário (Undo). O sistema precisa capturar o estado da entidade `Usuario` imediatamente antes da alteração ser efetivada e, caso o operador solicite, restaurar os dados originais no sistema e na persistência. Fazer isso diretamente no controlador misturaria a lógica de regras de negócio com o controle de histórico e violaria o encapsulamento da entidade, expondo seus atributos. A Sprint 5 também solicita a demonstração prática da aplicação de padrões de projeto comportamentais (GoF) para resolver esse tipo de problema.

## Decisão

Implementar a reversão combinando os padrões comportamentais **Command** e **Memento**:

- **Memento no Domínio:** Em `source/dominio/usuarios/`, a entidade `Usuario` atua como *Originator*. Ela ganha os métodos `criar_memento()` (que retorna um `UsuarioMemento` contendo uma cópia profunda, via `copy.deepcopy`, do seu `__dict__`) e `restaurar_memento(memento)`. O estado fica protegido e o domínio não conhece o histórico.
- **Command na Aplicação:** Em `source/aplicacao/comandos/`, criar a interface `Comando` genérica e a implementação `ComandoAtualizarUsuario`. Este comando captura a intenção da operação: antes de delegar a mutação ao `ControladorUsuario` (*Receiver*), ele solicita o Memento. Se a ação `desfazer()` for chamada, ele usa o Memento salvo para restaurar a entidade e solicita ao repositório que a atualize (rollback da persistência).
- **Zelador e Invocador na Fachada:** A classe `FacadeSingletonController` recebe o atributo `_ultimo_comando_desfazivel: Optional[Comando]`. Ao executar `atualizar_usuario`, a fachada instância o comando, executa-o e guarda sua referência (atuando como *Caretaker* e *Invoker*). O método `desfazer_ultima_atualizacao_usuario()` chama o desfazer do comando guardado e limpa o histórico.

## Consequências

- A entidade `Usuario` preserva seu encapsulamento, sendo a única que sabe como seu estado é extraído e injetado.
- O `ControladorUsuario` continua responsável apenas pelas regras de negócio e validações, respeitando o Princípio da Responsabilidade Única (SRP).
- Adicionar o suporte a um histórico maior (desfazer as últimas N ações) exigirá impacto quase zero: bastará alterar a variável da Fachada para uma estrutura de Pilha (`List`), sem precisar alterar o Domínio ou o Controlador.
- Introduz uma leve camada extra de abstração na aplicação, visto que o fluxo agora passa pela criação e execução de um objeto de comando antes de chegar ao controlador.

## Alternativas consideradas

- Guardar uma cópia do dicionário de dados diretamente no `ControladorUsuario`: rejeitada por ferir o encapsulamento da entidade (que teria seus atributos vazados) e por acoplar o gerenciamento de histórico na mesma classe que faz a validação de regras de negócio.
- Consultar o repositório de arquivo/banco de dados para resgatar o estado antigo: rejeitada porque os repositórios atuais gravam as alterações de forma atômica. Uma vez que o usuário foi atualizado, o arquivo binário antigo já foi sobrescrito pela escrita atômica (detalhada na ADR-0009).

## Relação com decisões anteriores

Esta decisão estende diretamente a **ADR-0008**, uma vez que a `FacadeSingletonController` absorve as novas responsabilidades de instanciar os comandos e atuar como o zelador do histórico de ações do sistema. Além disso, a reversão aciona a re-gravação no mecanismo de persistência definido pela **ADR-0009**, garantindo que as fábricas de arquivos binários e memória operem o *rollback* transparente dos dados revertidos.