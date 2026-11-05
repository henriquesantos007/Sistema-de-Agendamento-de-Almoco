# CRUD de Usuários

## Por quê

O CRUD de usuários foi implementado, mas os requisitos OpenSpec ainda
documentam apenas cadastro, listagem, validação e armazenamento. Esta mudança
registra a consulta por identificador, a atualização e a remoção de usuários,
além do tratamento da unicidade na atualização.

## O que muda

- Adiciona requisitos para consultar, atualizar e remover usuários.
- Estende o requisito de unicidade para impedir duplicidade durante a
  atualização sem considerar duplicados os dados que pertencem ao próprio
  usuário.
- Registra os casos de uso UC20 (Consultar Usuário) e UC21 (Remover Usuário);
  a atualização corresponde ao UC08 (Editar Usuário), já existente no
  catálogo.
- Atualiza os RNFs de segurança, usabilidade e confiabilidade para cobrir a
  senha na edição, mensagens de validação da atualização e rollback de falhas
  de persistência nas operações CRUD.

## Fora de escopo

- Alterar a implementação do CRUD ou os testes de código.
- Alterar a implementação de hashing de senha. Esta mudança atualiza NF-SEG-02
  para especificar o comportamento esperado na edição; a implementação desse
  comportamento permanece pendente.
- Alterar perfil, matrícula ou restaurante vinculado durante a atualização;
  a implementação atual mantém esses dados.
- Implementar interface web: as operações disponíveis no PR são exercitadas
  pelo cenário de demonstração em linha de comando.
