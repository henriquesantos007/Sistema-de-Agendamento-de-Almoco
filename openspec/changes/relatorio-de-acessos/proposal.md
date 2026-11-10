# Relatórios de Acesso

## Por quê

O projeto precisa apresentar estatísticas de acesso dos usuários. A
especificação deve definir o evento contado como acesso, o período consultado,
os dados apresentados e os formatos disponíveis antes da implementação.

## O que muda

- Especifica um relatório consolidado dos registros de acesso disponíveis,
  com quantidade total e quantidade por usuário.
- Define HTML e CSV como formatos do relatório, com os mesmos dados.
- Introduz o UC22 — Consultar Relatório de Acessos.

## Fora de escopo

- Implementar ou alterar o fluxo de autenticação.
- Definir como os eventos de acesso são capturados; o relatório consome os
  registros de acesso disponibilizados ao sistema.
- Definir o mecanismo de logging, os repositórios ou os padrões de projeto
  usados na implementação.
- Especificar interface web ou fluxo de distribuição dos arquivos gerados.
- Incluir filtros por período, gráficos ou detalhamento de dados pessoais.

## Premissas

- O Administrador é o perfil autorizado a solicitar o relatório.
- Cada registro de acesso disponível está associado a um usuário cadastrado.
- O relatório considera todos os registros de acesso disponibilizados, sem
  filtro de datas.
- O resumo contém o total de acessos e a quantidade de usuários distintos.
- O detalhamento identifica cada usuário por id, login, perfil e quantidade de
  acessos, sem incluir senha ou e-mail.
- Usuários sem registro de acesso não aparecem no detalhamento; quando não há
  registros, os totais são zero.
