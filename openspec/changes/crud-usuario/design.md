# Design: CRUD de Usuários

## Contexto

O `ControladorUsuario` delega consulta, atualização e remoção ao contrato
`RepositorioUsuarios`; as implementações em memória e em arquivo fornecem as
operações correspondentes. A `FacadeSingletonController` expõe essas ações
como `buscar_usuario`, `atualizar_usuario` e `remover_usuario`.

Na atualização, o controlador valida os dados com o identificador do próprio
usuário ignorado nas consultas de unicidade. O fluxo atual atualiza nome,
login, e-mail, senha e telefone, preservando identificador, perfil e os dados
específicos do perfil. Os requisitos documentais limitam-se a esse
comportamento implementado.

## Decisões

- Manter os requisitos canônicos em `openspec/specs/usuarios/spec.md` e
  registrar aqui o delta que os fundamenta.
- Reutilizar UC08 para edição e acrescentar UC20 para consulta individual e
  UC21 para remoção, sem renumerar casos de uso existentes.
- Tratar o identificador inexistente como recusa da operação; consulta,
  atualização e remoção usam a mesma mensagem de usuário não encontrado.
- Não descrever neste pacote a proteção de senha na atualização; essa regra
  pertence à especificação de segurança.

## Consequências

- RF06 passa a cobrir também a unicidade na atualização e evita falsos
  positivos para dados que já pertencem ao usuário editado.
- RF13–RF15 documentam consulta, atualização e remoção, incluindo o
  comportamento para identificadores inexistentes.
- Uma futura mudança que permita alterar perfil, matrícula ou restaurante do
  gestor deve atualizar RF14 e seus cenários.
