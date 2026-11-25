# Tarefas

- [x] Capturar o estado anterior e encapsular a atualização de usuário em um
  comando, delegando a alteração ao controlador (`feat(usuarios)`).
- [x] Expor o desfazimento de um passo na fachada e na CLI
  (`feat(cli)`).
- [x] Cobrir com teste de integração o desfazimento bem-sucedido e a ausência
  de histórico disponível (`test(usuarios)`).
- [x] Cobrir que duas atualizações consecutivas permitem desfazer somente a
  mais recente e que uma atualização inválida não descarta o histórico válido
  (`test(usuarios)`).
- [x] Invalidar o desfazimento quando o usuário correspondente for removido e
  cobrir a persistência do undo em arquivo (`test(usuarios)`).
- [x] Verificar falhas de persistência durante a atualização e o desfazimento,
  preservando o último estado persistido e permitindo nova tentativa
  (`test(usuarios)`).
- [x] Testar a cópia profunda do Memento e rejeitar sua restauração em entidade
  de classe ou identificador diferente (`test(usuarios)`).
- [x] Registrar os padrões Command e Memento na ADR e na documentação do
  projeto (`docs(arquitetura)`).
- [x] Incluir UC23 no catálogo e na matriz de rastreabilidade de casos de uso
  (`docs(casos-de-uso)`).
