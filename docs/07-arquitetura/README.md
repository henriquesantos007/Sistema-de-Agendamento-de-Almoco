# Arquitetura

Esta documentação descreve a implementação atual do repositório, um monólito
modular executado pela linha de comando. A visão de produto prevê uma aplicação
web, mas essa interface ainda não está implementada; os wireframes em
[06-interface](../06-interface/README.md) são conceituais.

- [Arquitetura lógica](./arquitetura-logica.md): camadas, responsabilidades e
  dependências.
- [Arquitetura física](./arquitetura-fisica.md): processo, ambiente de execução
  e persistência.
- [Atendimento dos RNFs](./atendimento-rnfs.md): relação de cada requisito não
  funcional com mecanismos e critérios de verificação.
- [ADR-0008 — Fachada Singleton](./adr/0008-fachada-singleton-dos-controladores.md):
  decisão de centralizar os controladores na fachada única.
- [ADR-0009 — Repository e Factory](./adr/0009-repository-e-factory-para-entidades-persistidas.md):
  decisão de usar contratos de repositório para as entidades persistidas,
  aceita para usuários e restaurantes; o Abstract Factory de repositórios e a
  extensão aos registros de acesso são propostos.
- [ADR-0010 — Adapter para logging](./adr/0010-adapter-para-logging.md):
  decisão proposta de isolar a biblioteca `logging` atrás de um Adapter.
- [ADR-0011 — Template Method para relatórios de acesso](./adr/0011-template-method-para-relatorios-de-acesso.md):
  decisão proposta de compartilhar o fluxo de geração dos relatórios HTML e
  CSV.

O diagrama de classes de projeto e os padrões estão em
[08-projeto.md](../08-projeto.md).
