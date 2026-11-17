# Tarefas

- [x] Capturar o estado anterior e encapsular a atualização de usuário em um
  comando, delegando a alteração ao controlador (`feat(usuarios)`).
- [x] Expor o desfazimento de um passo na fachada e na CLI
  (`feat(cli)`).
- [x] Cobrir com teste de integração o desfazimento bem-sucedido e a ausência
  de histórico disponível (`test(usuarios)`).
- [ ] Cobrir que duas atualizações consecutivas permitem desfazer somente a
  mais recente (`test(usuarios)`).
- [x] Registrar os padrões Command e Memento na ADR e na documentação do
  projeto (`docs(arquitetura)`).
- [ ] Documentar o UC23 — Desfazer atualização de usuário em
  `docs/04-casos-de-uso/detalhados.md` (`docs(casos-de-uso)`).
