# Design: CRUD de Restaurantes e Fachada

## Contexto da implementação

O sistema é um monólito modular em camadas. `main.py` escolhe as
implementações dos repositórios por meio de `fabrica_repositorio.py`; a
`FacadeSingletonController` reúne o `ControladorUsuario` e o
`ControladorRestaurante`. Os controladores dependem dos contratos do domínio,
não das implementações de persistência.

O CRUD de Restaurante valida `DadosRestaurante`, gera a entidade, e delega as
operações ao `RepositorioRestaurantes`. O vínculo do `GestorRestaurante` é
validado no cadastro de usuário; uma remoção de restaurante é recusada se
houver gestor associado. A fachada soma as contagens dos repositórios para
expor o resumo de entidades.

## Decisões

- Manter os requisitos RF07–RF12 e NF-MAN-02 na localização canônica
  `openspec/specs/`. O delta deste pacote é uma cópia histórica dos requisitos
  já aceitos, não uma segunda alteração a ser aplicada sobre as specs atuais.
- Manter a persistência intercambiável por meio de contratos e da fábrica.
- Usar a fachada Singleton como ponto único de acesso no fluxo de produção.
- Preservar a restrição de não remover restaurante vinculado a gestor.
- Registrar a decisão da fachada no
  [ADR-0008](../../../../docs/07-arquitetura/adr/0008-fachada-singleton-dos-controladores.md);
  não é necessária uma nova decisão arquitetural.

## Arquivamento

O pacote foi arquivado com
`openspec archive crud-restaurante --skip-specs --yes`. A opção `--skip-specs`
evita reaplicar os deltas, que registram requisitos já presentes nas
especificações canônicas.

## Alternativas consideradas

- **Duplicar ou renumerar requisitos nas specs canônicas:** rejeitado porque
  RF07–RF12 e NF-MAN-02 já estão especificados.
- **Fazer a fachada instanciar os repositórios concretos:** rejeitado por
  acoplar aplicação à infraestrutura e duplicar a responsabilidade da fábrica.
- **Remover restaurantes mesmo com gestores vinculados:** rejeitado para
  preservar a integridade da associação.

## Riscos e consequências

- A fachada é estado único por processo; testes devem reiniciá-la para não
  compartilhar estado acidentalmente.
- A implementação atual usa arquivos `pickle`, que devem ser tratados como
  confiáveis e locais.
- A documentação de wireframes é conceitual; a interface em execução continua
  sendo a CLI.
