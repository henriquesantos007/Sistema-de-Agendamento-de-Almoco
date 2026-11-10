# ADR-0010: Adaptar a biblioteca de logging

- Status: Proposto
- Data: 2026-11-10

## Contexto

A aplicação precisa registrar eventos operacionais sem acoplar suas regras a
uma biblioteca específica de logging. A Sprint 4 solicita demonstrar o padrão
Adapter em um cenário do projeto. Ainda não há integração de logging no código.

## Decisão proposta

- Definir na aplicação um contrato pequeno de logging, com os níveis e as
  operações necessários aos eventos do sistema.
- Implementar na infraestrutura um Adapter que recebe esse contrato e delega
  os registros à biblioteca `logging` da biblioteca padrão do Python,
  convertendo níveis e mensagens conforme necessário.
- Configurar o Adapter na composição da aplicação, sem fazer controladores ou
  serviços importarem diretamente a biblioteca de logging.
- Usar como cenário inicial o registro de que um relatório foi gerado,
  incluindo o formato e o resultado da operação. Falhas operacionais relevantes
  também podem ser registradas.
- Não incluir senhas, hashes, e-mails ou outros dados pessoais nas mensagens.
- Não usar arquivos de log como fonte das estatísticas de acesso. Os relatórios
  devem consultar os registros de acesso mantidos para esse fim.

Esta integração é uma decisão planejada; não significa que o Adapter ou os
eventos de logging já estejam implementados.

## Consequências

- A aplicação depende de um contrato estável, e não da API concreta da
  biblioteca de logging.
- A implementação pode trocar ou configurar o destino do logging na
  infraestrutura sem alterar as regras de negócio.
- O uso da biblioteca padrão evita adicionar dependência externa para este
  cenário.
- Os testes podem verificar os eventos enviados ao contrato sem depender da
  saída real do logger.
- A equipe deve definir os níveis e destinos de saída necessários durante a
  implementação, evitando registrar informações sensíveis.

## Alternativas consideradas

- Chamar `logging` diretamente nos controladores e serviços; rejeitada por
  acoplar a aplicação à biblioteca e dificultar sua substituição ou teste.
- Usar os logs como registros de acesso para calcular estatísticas; rejeitada
  porque logs operacionais não constituem o armazenamento estruturado e
  consultável exigido pelo relatório.
- Adicionar uma biblioteca externa de logging; não adotada nesta decisão,
  pois a biblioteca padrão atende ao cenário mínimo sem nova dependência.
