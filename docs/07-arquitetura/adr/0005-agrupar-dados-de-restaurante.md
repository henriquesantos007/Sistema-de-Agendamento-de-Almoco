# ADR-0005: Agrupar os dados editáveis de restaurante

- Status: Aceito
- Data: 2026-10-27

## Contexto

O construtor de `Restaurante` e o método `atualizar_dados` recebiam os mesmos
cinco dados editáveis em parâmetros separados. Isso ultrapassava a recomendação
de quantidade de parâmetros do guia de contribuição e repetia a assinatura em
cada chamada.

## Decisão

Agrupar nome, descrição, localização, telefone e horário limite de agendamento
em `DadosRestaurante`, um objeto de valor imutável. `Restaurante` recebe esse
objeto ao ser criado e atualizado. O identificador, o status inicial e a data
de cadastro permanecem responsabilidade da entidade e do repositório, e não
fazem parte dos dados editáveis.

## Consequências

- O construtor de `Restaurante` e `atualizar_dados` recebem um único argumento
  de dados.
- A criação e a atualização usam a mesma estrutura tipada.
- Chamadores da assinatura anterior devem migrar para `DadosRestaurante`.
