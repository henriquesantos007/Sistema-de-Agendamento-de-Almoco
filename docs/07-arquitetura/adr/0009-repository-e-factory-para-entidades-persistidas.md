# ADR-0009: Aplicar Repository e Factory às entidades persistidas

- Status: Aceito
- Data: 2026-11-10

## Contexto

Os controladores e validadores precisam consultar e alterar dados sem depender
de como eles são armazenados. O projeto já definia `RepositorioUsuarios` e
`RepositorioRestaurantes` como contratos no domínio, implementados em memória
e em arquivo na infraestrutura.

Até esta decisão, a escolha da implementação ocorria no início da execução
pelas funções de módulo `criar_repositorio_usuarios` e
`criar_repositorio_restaurantes`, em
`source/infraestrutura/persistencia/fabrica_repositorio.py`, que recebiam
`armazenamento` (`memoria` ou `arquivo`) e um `caminho` opcional. Cada função
decidia por um `if` sobre `armazenamento`, sem classe de fábrica instanciável.
Esse arranjo era uma fábrica simples, não um Factory Method nem um Abstract
Factory no sentido do GoF.

A Sprint 4 solicita Repository para as entidades do projeto e Factory Method
ou Abstract Factory para criar entidades ou escolher o tipo de repositório. A
change `relatorio-de-acessos` calcula estatísticas a partir de registros de
acesso, que também precisam de persistência; a captura desses registros fica
fora dessa change.

## Decisão

- Para cada entidade de domínio que tenha persistência própria, definir um
  contrato de repositório no domínio. A aplicação depende desses contratos, e
  não importa implementações concretas da infraestrutura.
- Implementar os contratos na infraestrutura, mantendo cada mecanismo de
  armazenamento substituível sem alterar as regras de negócio.
- Substituir a fábrica simples por um Abstract Factory, em
  `source/infraestrutura/persistencia/fabrica_repositorios.py`:
  `FabricaRepositorios`, abstrata, com os métodos de criação
  `criar_repositorio_usuarios()`, `criar_repositorio_restaurantes()` e
  `criar_repositorio_acessos()`, e as fábricas concretas
  `FabricaRepositoriosMemoria` e `FabricaRepositoriosArquivo`. Esta última
  recebe os caminhos dos arquivos de usuários, restaurantes e acessos; sem
  valor, usa `dados/usuarios.bin`, `dados/restaurantes.bin` e
  `dados/acessos.jsonl`. As funções de `fabrica_repositorio.py` foram
  removidas.
- Escolher a fábrica concreta a partir de `armazenamento` em um único ponto da
  composição da aplicação: `escolher_fabrica`, no `main.py`, que também monta a
  fachada. Os repositórios obtidos da fábrica são entregues à fachada, que não
  conhece a fábrica (ADR-0008).
- Aplicar o mesmo desenho ao registro de acesso: contrato `RepositorioAcessos`
  no domínio e implementações em memória e em arquivo na infraestrutura,
  criadas pelas fábricas concretas. Registros de acesso são imutáveis: o
  contrato só registra e lista, sem atualizar nem remover.
- Persistir os acessos em arquivo por acréscimo: `RepositorioAcessosArquivo`
  acrescenta cada registro ao fim do arquivo, uma linha JSON por registro, sem
  reescrever os anteriores. Por isso implementa `RepositorioAcessos`
  diretamente e não herda de `RepositorioAcessosMemoria`, ao contrário dos
  repositórios de usuários e restaurantes. O motivo é que o dado de acesso só
  cresce e nunca é editado; regravar o arquivo inteiro a cada acesso custaria
  proporcionalmente ao histórico.
- O registro guarda apenas o id do usuário; login e perfil são resolvidos no
  repositório de usuários na hora do relatório. Isso pressupõe que os ids de
  usuário não são reaproveitados durante a vida do armazenamento de acessos e
  que os armazenamentos de usuários e de acessos são usados sempre em
  conjunto; recriar ou trocar o de usuários mantendo o de acessos atribuiria
  acessos antigos a outro usuário.
- Manter a criação das entidades nas regras de domínio ou de aplicação; a
  fábrica seleciona repositórios, não substitui os construtores das entidades.
- Interpretar "todas as entidades" como todas as entidades que exijam
  armazenamento independente no escopo implementado. Objetos de valor e dados
  derivados de consultas não recebem repositórios próprios sem necessidade
  de persistência.

## Consequências

- Controladores e validadores podem ser testados com implementações em memória
  ou substitutos dos contratos sem conhecer detalhes de arquivo.
- A infraestrutura permanece responsável por detalhes de armazenamento e
  pelas implementações concretas.
- Com o Abstract Factory, os três repositórios de uma execução saem da mesma
  família de armazenamento, e a decisão sobre `armazenamento` não se repete
  em cada método de criação.
- Uma nova entidade persistida exige contrato, implementação(ões), um método
  de criação em cada fábrica e testes correspondentes.
- Um novo mecanismo de armazenamento exige uma nova fábrica concreta, sem
  alterar as existentes.
- O arquivo de acessos usa um formato de texto, diferente dos arquivos
  binários de usuários e restaurantes, e é lido em `listar_todos`; uma linha
  inválida gera `ErroPersistencia` com o número da linha. Depois de uma escrita
  interrompida, o registro seguinte começa em nova linha, mas a linha truncada
  continua inválida.
- Uma trava serializa as gravações de acessos entre threads do mesmo processo.
  Processos diferentes gravando o mesmo arquivo continuam sem proteção, como os
  demais repositórios (ADR-0008).

## Alternativas consideradas

- Manter as funções de módulo de `fabrica_repositorio.py` e acrescentar
  `criar_repositorio_acessos`; rejeitada porque é uma fábrica simples, não
  Factory Method nem Abstract Factory como pede a Sprint 4, repete o `if`
  sobre `armazenamento` em cada função e não impede combinar mecanismos
  diferentes para entidades da mesma execução.
- Reaproveitar para os acessos a regravação total em binário das ADR-0003 e
  ADR-0006, com `RepositorioAcessosArquivo` herdando da versão em memória;
  rejeitada porque cada novo registro regravaria todo o histórico, e os
  registros de acesso nunca são editados.
- Factory Method, com uma classe criadora por repositório; rejeitada porque a
  escolha do armazenamento vale para a família inteira de repositórios, o que
  o Abstract Factory expressa diretamente.
- Fazer controladores acessarem diretamente as implementações de arquivo ou
  memória; rejeitada por acoplar as regras da aplicação aos detalhes de
  infraestrutura.
- Criar uma fábrica diferente em cada controlador; rejeitada por espalhar a
  seleção do armazenamento e dificultar a composição consistente.
- Criar repositórios para todo tipo de classe, incluindo objetos de valor e
  resultados calculados; rejeitada porque Repository se aplica a dados com
  ciclo de vida e persistência próprios, não a toda classe do modelo.
- Fazer a fábrica criar entidades de domínio; rejeitada porque a criação das
  entidades deve continuar sob responsabilidade das regras que conhecem suas
  invariantes, enquanto esta fábrica escolhe o mecanismo de persistência.

## Relação com decisões anteriores

Esta decisão consolida e estende o desenho já registrado em
[ADR-0003](./0003-persistencia-de-usuarios-em-binario.md) para usuários e em
[ADR-0006](./0006-persistencia-de-restaurantes-em-arquivo.md) para restaurantes.
Não altera os mecanismos de armazenamento de usuários e restaurantes; substitui
a forma de escolhê-los, descrita naquelas ADRs pelas funções de
`fabrica_repositorio.py`, e adota, só para os acessos, a gravação por
acréscimo. Mantém a regra da
[ADR-0008](./0008-fachada-singleton-dos-controladores.md) de que a fachada
recebe os repositórios e não usa a fábrica.
