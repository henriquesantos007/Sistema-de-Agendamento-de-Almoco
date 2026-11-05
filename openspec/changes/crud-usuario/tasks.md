# Tarefas

- [x] Conferir as operações de usuário implementadas no controlador,
  repositórios e fachada.
- [x] Atualizar a especificação canônica para refletir unicidade na
  consulta, atualização e remoção de usuários.
- [x] Registrar no delta OpenSpec os requisitos RF06 e RF13–RF15.
- [x] Documentar os limites da atualização atualmente implementada.
- [x] Estender NF-SEG-02 para exigir hash também na atualização.
- [x] Estender NF-USA-01 para cobrir a atualização recusada por múltiplos
  motivos.
- [ ] Implementar e testar a geração de hash da senha durante a atualização.
- [x] Estender NF-CON-01 para cobrir falhas de persistência na atualização e
  remoção de usuários.
- [x] Alinhar a matriz de RNFs e o ADR-0003 ao comportamento e à garantia
  esperada para as operações em arquivo.
- [ ] Corrigir e testar o rollback da atualização quando a gravação falhar.
- [ ] Testar rollback da remoção de usuário quando a gravação falhar.
- [x] Atualizar os diagramas de análise, projeto e arquitetura lógica com o
  CRUD de usuários e a validação de unicidade por `id_ignorado`.
