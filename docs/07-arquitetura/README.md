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

O diagrama de classes de projeto e os padrões estão em
[08-projeto.md](../08-projeto.md).
