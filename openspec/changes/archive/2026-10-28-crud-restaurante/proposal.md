# CRUD de Restaurantes e Resumo de Entidades

## Why (Por quê)

O CRUD de restaurantes e a fachada única já foram implementados, mas faltava
manter no OpenSpec um pacote de mudança rastreável junto à documentação dos
casos de uso, telas e arquitetura. Esta mudança registra os requisitos e a
decisão arquitetural que fundamentam a entrega.

## What Changes (O que muda)

- Consolida os requisitos de cadastro, consulta, listagem, atualização e
  remoção de restaurantes, incluindo o vínculo com gestores.
- Registra o resumo de contagem de usuários e restaurantes oferecido pela
  fachada.
- Documenta as fronteiras de uso da fachada Singleton e os artefatos de
  interface e arquitetura associados ao CRUD.

Não há alteração de comportamento de produção nesta documentação: os
requisitos RF07–RF12 e NF-MAN-02 já estão nas especificações canônicas e as
operações já estão implementadas.

## Fora de escopo

- Implementar cardápios, pratos, agendamentos, pedidos ou pagamentos.
- Implementar a aplicação web prevista na visão do produto.
- Alterar as regras de cadastro de usuários ou o formato de persistência.
