# ADR-0010: Adaptar a biblioteca de logging

- Status: Aceito
- Data: 2026-11-10

## Contexto

A aplicação precisa registrar eventos operacionais sem acoplar suas regras a
uma biblioteca específica de logging. A Sprint 4 solicita demonstrar o padrão
Adapter em um cenário do projeto. Até esta decisão, não havia integração de
logging no código.

## Decisão

- Definir na aplicação um contrato pequeno de logging, `LoggerAplicacao`, em
  `source/aplicacao/logger_aplicacao.py`, com a operação
  `registrar(evento, detalhes, nivel)`. O terceiro parâmetro é opcional e usa a
  enumeração `NivelEvento` (`INFORMACAO`, o padrão, `AVISO` e `ERRO`), também
  definida na aplicação.
- Implementar na infraestrutura um Adapter, `AdaptadorLogging`, em
  `source/infraestrutura/logs/`, que implementa esse contrato e delega os
  registros à biblioteca `logging` da biblioteca padrão do Python, convertendo
  `NivelEvento` nos níveis `INFO`, `WARNING` e `ERROR`.
- Configurar o Adapter na composição da aplicação: o `main.py` o obtém por
  `criar_adaptador_logging()`, que configura a saída do logger da aplicação, e
  o entrega à fachada. Controladores e serviços não importam a biblioteca de
  logging.
- Usar como cenário inicial o relatório de acessos. O `ServicoRelatorioAcesso`
  registra a geração como informação, apenas com o formato normalizado; a
  recusa de formato como aviso, sem o formato digitado, que é entrada livre; e
  a falha de persistência durante a geração como erro.
- Não incluir senhas, hashes, e-mails ou outros dados pessoais nas mensagens.
- Não usar arquivos de log como fonte das estatísticas de acesso. Os relatórios
  consultam os registros de acesso mantidos para esse fim.

## Consequências

- A aplicação depende de um contrato estável, e não da API concreta da
  biblioteca de logging.
- A implementação pode trocar ou configurar o destino do logging na
  infraestrutura sem alterar as regras de negócio.
- O uso da biblioteca padrão evita adicionar dependência externa para este
  cenário.
- Os testes podem verificar os eventos enviados ao contrato sem depender da
  saída real do logger.
- O nível do evento faz parte do contrato; um novo nível exige alterar
  `NivelEvento` e a conversão do Adapter.

## Alternativas consideradas

- Chamar `logging` diretamente nos controladores e serviços; rejeitada por
  acoplar a aplicação à biblioteca e dificultar sua substituição ou teste.
- Usar os logs como registros de acesso para calcular estatísticas; rejeitada
  porque logs operacionais não constituem o armazenamento estruturado e
  consultável exigido pelo relatório.
- Adicionar uma biblioteca externa de logging; não adotada nesta decisão,
  pois a biblioteca padrão atende ao cenário mínimo sem nova dependência.
