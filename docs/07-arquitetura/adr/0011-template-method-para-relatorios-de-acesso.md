# ADR-0011: Gerar os relatórios de acesso com Template Method

- Status: Proposto
- Data: 2026-11-10

## Contexto

A change `relatorio-de-acessos` especifica um relatório de acessos em HTML e
CSV (RF16 e RF17). Os dois formatos precisam apresentar os mesmos dados: total
de acessos, quantidade de usuários distintos e detalhamento por usuário, na
mesma ordem. O fluxo é fixo: consultar os registros de acesso, consultar login
e perfil dos usuários, calcular as estatísticas e, por fim, formatar o
resultado. Só o último passo varia com o formato. A Sprint 4 solicita
demonstrar o padrão Template Method em um cenário do projeto. Ainda não há
relatórios no código.

## Decisão proposta

- Definir na aplicação a classe abstrata `TemplateRelatorioAcesso`, cujo
  método `gerar()` fixa o fluxo: chama `obter_estatisticas()` e, com o
  resultado, `formatar(estatisticas)`.
- Implementar `obter_estatisticas()` uma única vez na classe base, consultando
  `RepositorioAcessos` e `RepositorioUsuarios` e produzindo um
  `EstatisticasAcesso`.
- Deixar `formatar()` abstrato e especializá-lo em `RelatorioAcessoHTML` e
  `RelatorioAcessoCSV`, que produzem um `Documento` com o conteúdo textual no
  formato correspondente.
- Fazer o `ServicoRelatorioAcesso` escolher a subclasse pelo formato pedido e
  instanciá-la com os dois repositórios. Formatos diferentes de HTML e CSV são
  recusados pelo serviço antes de qualquer consulta.

Esta decisão é planejada; não significa que o template, os formatos ou o
serviço já estejam implementados.

## Consequências

- O cálculo das estatísticas fica em um só lugar, e os dois formatos partem do
  mesmo `EstatisticasAcesso`, o que sustenta a exigência de mesmos dados do
  RF17.
- Um novo formato exige uma subclasse com `formatar()` e o registro dela no
  serviço, sem alterar o cálculo.
- As subclasses ficam acopladas à classe base por herança; mudanças no fluxo
  de `gerar()` afetam todos os formatos.
- Os testes podem verificar o cálculo uma vez na classe base e, em cada
  formato, apenas a formatação.

## Alternativas consideradas

- Strategy por formato, com um gerador único que recebe um formatador
  injetado; viável e com menor acoplamento por herança, mas não adotada porque
  a variação se limita a um passo de um fluxo fixo e a Sprint 4 pede a
  demonstração do Template Method. Se a variação passar a envolver mais de um
  passo ou combinações independentes, Strategy deve ser reavaliada.
- Um `if` por formato dentro do serviço; rejeitada por misturar a coordenação
  do caso de uso com a apresentação e crescer a cada novo formato.
- Uma classe por formato sem base comum; rejeitada por duplicar a consulta e o
  cálculo das estatísticas em cada formato.

## Relação com decisões anteriores

Os repositórios consultados seguem a
[ADR-0009](./0009-repository-e-factory-para-entidades-persistidas.md), e o
registro do resultado da geração usa o contrato de logging da
[ADR-0010](./0010-adapter-para-logging.md).
