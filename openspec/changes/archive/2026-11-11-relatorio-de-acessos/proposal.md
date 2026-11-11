# Relatórios de Acesso

## Por quê

O projeto precisa apresentar estatísticas de acesso dos usuários. Esta change
especifica os dados apresentados e os formatos disponíveis do relatório,
calculado sobre os registros de acesso disponíveis, antes da implementação. O
evento que origina cada registro fica para a change que implementar a captura.

## O que muda

- Especifica um relatório consolidado dos registros de acesso disponíveis,
  com quantidade total e quantidade por usuário.
- Define HTML e CSV como formatos do relatório, com os mesmos dados.
- Introduz o UC22 — Consultar Relatório de Acessos.

## Fora de escopo

- Implementar ou alterar o fluxo de autenticação.
- Definir como os eventos de acesso são capturados; o relatório consome os
  registros de acesso disponibilizados ao sistema.
- Fixar nos requisitos o mecanismo de logging, os repositórios ou os padrões
  de projeto usados na implementação; essas escolhas ficam no `design.md` e nas
  ADR-0009, ADR-0010 e ADR-0011.
- Especificar interface web ou fluxo de distribuição dos arquivos gerados.
- Incluir filtros por período, gráficos ou detalhamento de dados pessoais.

## Premissas

- O Administrador é o perfil autorizado a solicitar o relatório.
- Um registro de acesso representa um acesso de um usuário em um instante e
  guarda o id desse usuário. O projeto não tem fluxo de login; o evento que
  origina o registro será definido pela change que implementar a captura.
- O usuário de um registro pode ter sido removido depois do acesso (UC21,
  RF15). Os registros de um usuário removido continuam contando no total de
  acessos e na quantidade de usuários distintos; no detalhamento, a linha
  mostra o id e indica login e perfil como "usuário removido".
- O login e o perfil são obtidos dos usuários cadastrados no momento do
  relatório, a partir do id guardado no registro. Isso pressupõe que os
  identificadores de usuário não são reaproveitados durante a vida do
  armazenamento de acessos e que os armazenamentos de usuários e de acessos
  são usados sempre em conjunto. Recriar ou trocar o armazenamento de usuários
  mantendo o de acessos atribuiria acessos antigos a outro usuário.
- Registros de acesso não são alterados nem removidos depois de registrados.
- O relatório considera todos os registros de acesso disponibilizados, sem
  filtro de período.
- O resumo contém o total de acessos e a quantidade de usuários distintos.
- O detalhamento identifica cada usuário por id, login, perfil e quantidade de
  acessos, sem incluir senha ou e-mail.
- Usuários sem registro de acesso não aparecem no detalhamento; quando não há
  registros, os totais são zero.
