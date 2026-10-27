# ADR-0008: Centralizar os controladores em uma fachada Singleton

- Status: Aceito
- Data: 2026-10-27

## Contexto

O `main.py` montava manualmente os validadores, os controladores e os
repositórios, e chamava cada controlador diretamente. Com
`ControladorUsuario` e `ControladorRestaurante`, que dependem dos repositórios
um do outro (o validador de gestores consulta restaurantes e o controlador de
restaurantes consulta usuários), essa montagem se repete em cada cliente e
expõe detalhes internos. O Sprint 3 pede uma fachada única para os
controladores, com Singleton, e um método que retorne a quantidade de
entidades cadastradas.

## Decisão

Criar `FacadeSingletonController` em `source/aplicacao/fachada/`.

- **Facade:** expõe as operações de usuários e o CRUD de restaurantes e monta
  internamente validadores e controladores. O `main.py` passa a conhecer apenas
  a fachada.
- **Singleton:** a instância única é obtida por `obter_instancia`. O construtor
  direto levanta `TypeError`, a criação é protegida por trava e `reiniciar()`
  descarta a instância para testes ou troca de armazenamento.
- **Configuração:** os repositórios, que são as abstrações do domínio, são
  informados na primeira chamada de `obter_instancia`. Assim a camada de
  aplicação não importa a infraestrutura, e a escolha do armazenamento continua
  na fábrica, chamada pelo `main.py`. Chamadas seguintes sem argumentos devolvem
  a mesma instância; repositórios diferentes dos usados na criação levantam
  `ValueError`, para a configuração não ser ignorada em silêncio.
- **Contagem:** adicionar `contar()` ao contrato `RepositorioUsuarios` (que já
  existia em `RepositorioRestaurantes`), implementado no repositório em memória
  e herdado pelo de arquivo, e expor `contar()` nos dois controladores.
  `contar_total_entidades()` soma usuários e restaurantes;
  `contar_usuarios()`, `contar_restaurantes()` e
  `obter_contagem_por_entidade()` dão o detalhe.

## Consequências

- Os clientes dependem de uma única classe, e a montagem dos controladores fica
  em um só lugar.
- O contrato público `RepositorioUsuarios` ganha um método abstrato: toda nova
  implementação precisa fornecer `contar()`.
- Há estado global: existe uma fachada por processo, e os testes devem chamar
  `reiniciar()` para não vazar estado entre si.
- Novas entidades devem ser incluídas em `obter_contagem_por_entidade()` para
  entrar na soma total.
- A fachada tende a crescer com cada nova entidade; se ficar extensa, pode ser
  dividida em subfachadas.
- Apenas a criação da instância é protegida contra concorrência; os
  repositórios continuam sem tratar acesso simultâneo.
- Os controladores continuam acessíveis nos seus pacotes; usar a fachada é uma
  convenção da equipe, não uma restrição técnica.

## Alternativas consideradas

- Implementar o Singleton com `__new__` devolvendo sempre o mesmo objeto;
  rejeitada porque o `__init__` rodaria a cada chamada e poderia reconfigurar
  ou zerar o estado.
- Usar uma variável global ou um módulo; rejeitada por não controlar a
  configuração inicial e dificultar os testes.
- Fazer a fachada criar os repositórios pela fábrica; rejeitada por acoplar a
  camada de aplicação à infraestrutura.
- Contar com `len(listar_todos())`; rejeitada por copiar a lista inteira
  apenas para contar, enquanto `contar()` já existia para restaurantes.
