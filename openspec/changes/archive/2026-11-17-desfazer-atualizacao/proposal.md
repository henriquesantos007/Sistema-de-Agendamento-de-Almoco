# Desfazer atualização de usuário

## Por quê

A Sprint 5 requer que o Administrador possa reverter a última atualização de
um usuário. Sem esse fluxo, uma alteração confirmada por engano só pode ser
corrigida com uma nova atualização manual.

## O que muda

- Define o desfazimento da atualização concluída mais recentemente para um
  usuário, restaurando o estado anterior e persistindo a restauração.
- Define o comportamento quando não há atualização disponível para desfazer
  e o limite de uma única ação de desfazimento.
- Associa o fluxo ao UC23 — Desfazer atualização de usuário.

## Fora de escopo

- Desfazer cadastro ou remoção de usuários, ou operações de outras entidades.
- Manter histórico de desfazimentos após o encerramento do processo.
- Desfazer mais de uma atualização ou refazer uma ação desfeita.
- Criar uma interface web para o fluxo.
