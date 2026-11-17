# Design: Desfazer atualização de usuário

## Contexto

A atualização de usuário é coordenada pela `FacadeSingletonController` e
executada pelo `ControladorUsuario`, que aplica as validações e persiste os
dados. O desfazimento precisa preservar essas responsabilidades e permitir
restaurar o estado anterior sem expor o histórico ao controlador.

## Decisões

- Encapsular a atualização em um comando, que captura o estado do usuário
  antes de executar a alteração.
- Usar um Memento criado pela entidade `Usuario` para guardar o estado anterior
  sem transferir ao controlador a responsabilidade de conhecer os atributos
  internos da entidade.
- Manter na fachada somente o comando da última atualização concluída com
  sucesso. Uma atualização posterior substitui esse comando; o desfazimento
  executa a restauração e limpa o histórico de um passo.
- Quando não há comando disponível, a fachada informa que nada pode ser
  desfeito sem alterar os usuários.
- Registrar a decisão arquitetural na
  [ADR-0012](../../../docs/07-arquitetura/adr/0012-command-e-memento-para-desfazer.md).

## Consequências

- O controlador continua responsável pelas regras de negócio da atualização,
  enquanto a fachada coordena o comando e seu histórico de um passo.
- O histórico existe somente durante a execução atual do processo; reiniciar o
  sistema elimina a possibilidade de desfazer a atualização anterior.
- O fluxo pode ser exercitado pela CLI sem adicionar dependências à interface.
