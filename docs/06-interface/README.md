# Wireframes da Interface

Os wireframes abaixo descrevem a interface web conceitual para os casos de uso
**UC05**, **UC08**, **UC12**, **UC16**, **UC20** e **UC21**, selecionados em
[casos de uso detalhados](../04-casos-de-uso/detalhados.md). São referências
para uma interface futura; a interface executável atual é a linha de comando
do `main.py`.

## UC05 — Cadastrar Usuário

```text
+------------------------------------------------------------------+
| Sistema de Agendamento de Almoços                  Administrador |
| Usuários > Cadastrar                                             |
+------------------------------------------------------------------+
| Perfil *                                                         |
| [ Estudante                         v ]                          |
|                                                                  |
| Nome *                  Login *                                  |
| [____________________]  [____________]                           |
| E-mail *                Telefone *                               |
| [____________________]  [____________]                           |
| Senha *                                                         |
| [••••••••••••••••••••]  (mostrar senha)                          |
| Matrícula *                                                     |
| [____________________]                                            |
|                                                                  |
| [Cancelar]                                      [Cadastrar]     |
+------------------------------------------------------------------+
| Mensagens de validação aparecem aqui, agrupadas por campo.       |
+------------------------------------------------------------------+
```

Quando o perfil selecionado for **Gestor de Restaurante**, o campo
**Matrícula** é substituído por **Restaurante vinculado** (seleção de um
restaurante existente). Para **Administrador**, os campos específicos de
perfil não são exibidos. A senha é mascarada e nunca aparece em mensagens de
sucesso ou listagens.

## UC20 — Consultar Usuário

```text
+------------------------------------------------------------------+
| Sistema de Agendamento de Almoços                  Administrador |
| Usuários > Detalhes                                              |
+------------------------------------------------------------------+
| ID: 1                    Perfil: Estudante                       |
| Nome: Victor Silva                                               |
| Login: victor                                                    |
| E-mail: victor@ci.ufpb.br                                         |
| Telefone: (83) 99999-0000                                         |
| Matrícula: 2026001                                                |
| Senha: [não exibida]                                              |
|                                                                  |
| [Voltar]       [Editar usuário]                 [Remover usuário] |
+------------------------------------------------------------------+
```

Os dados específicos do perfil são exibidos como informação, sem ação para
alterá-los. A senha e seu hash nunca aparecem na consulta.

## UC08 — Editar Usuário

```text
+------------------------------------------------------------------+
| Sistema de Agendamento de Almoços                  Administrador |
| Usuários > Editar                                                |
+------------------------------------------------------------------+
| ID: 1                    Perfil: Estudante (não editável)         |
|                                                                  |
| Nome *                  Login *                                  |
| [Victor Silva_______]   [victor_______]                          |
| E-mail *                Telefone *                               |
| [victor@ci.ufpb.br___]  [83999990000___]                         |
| Nova senha *                                                     |
| [••••••••••••••••••••]  (mostrar senha)                          |
| Matrícula: 2026001 (não editável)                                |
|                                                                  |
| [Cancelar]                                   [Salvar alterações] |
+------------------------------------------------------------------+
| Os motivos de validação são exibidos juntos, sem alterar os dados.|
+------------------------------------------------------------------+
```

O perfil e os dados específicos dele (matrícula de Estudante ou restaurante
vinculado de Gestor) são preservados na edição. A validação de unicidade
desconsidera os dados que já pertencem ao usuário editado. A senha é
obrigatória pela validação atual, deve ficar mascarada e nunca deve aparecer
em mensagens. A implementação atual ainda precisa gerar hash ao atualizar a
senha, conforme [NF-SEG-02](../../openspec/specs/rnf/seguranca/spec.md).

## UC21 — Remover Usuário

```text
+------------------------------------------------------------------+
| Sistema de Agendamento de Almoços                  Administrador |
| Usuários > Detalhes                                              |
+------------------------------------------------------------------+
| ID: 1                    Perfil: Estudante                       |
| Nome: Victor Silva                                               |
| Login: victor                                                    |
| E-mail: victor@ci.ufpb.br                                         |
|                                                                  |
| [Voltar]                                      [Remover usuário]  |
+------------------------------------------------------------------+
| Confirmação                                                      |
| Remover o usuário "Victor Silva" (ID 1)?                         |
| Esta ação não pode ser desfeita.                                 |
| [Cancelar]                                  [Confirmar remoção]   |
+------------------------------------------------------------------+
```

Após a confirmação, a interface atualiza a listagem e a contagem de usuários.
Se o identificador não existir, informa que o usuário não foi encontrado e
mantém a listagem.

## UC12 — Cadastrar Restaurante

```text
+------------------------------------------------------------------+
| Sistema de Agendamento de Almoços                  Administrador |
| Restaurantes > Cadastrar                                         |
+------------------------------------------------------------------+
| Nome *                                                           |
| [______________________________________________________________] |
| Descrição                                                        |
| [______________________________________________________________] |
| [______________________________________________________________] |
| Localização *                                                    |
| [______________________________________________________________] |
| Telefone *                 Horário limite de agendamento *       |
| [____________________]     [ HH:MM ]                             |
|                                                                  |
| [Cancelar]                                      [Cadastrar]     |
+------------------------------------------------------------------+
| Campos obrigatórios marcados com *. Erros são exibidos juntos.  |
| Após salvar: restaurante ativo, com ID e data gerados pelo sistema. |
+------------------------------------------------------------------+
```

## UC16 — Remover Restaurante

```text
+------------------------------------------------------------------+
| Sistema de Agendamento de Almoços                  Administrador |
| Restaurantes > Detalhes                                          |
+------------------------------------------------------------------+
| Restaurante: Restaurante do CI                                    |
| ID: 1                    Status: ATIVO                            |
| Localização: Centro de Informática                               |
| Telefone: (83) 97777-0000                                         |
|                                                                  |
| Gestores vinculados: nenhum                                       |
|                                                                  |
| [Voltar]                                      [Remover restaurante]|
+------------------------------------------------------------------+
| Confirmação                                                      |
| Remover "Restaurante do CI" (ID 1)? Esta ação não pode ser       |
| desfeita.                                                        |
| [Cancelar]                                  [Confirmar remoção]   |
+------------------------------------------------------------------+
```

Se houver gestor vinculado, a ação de remover é bloqueada e a tela deve
informar que o vínculo precisa ser removido antes. Se o restaurante não
existir, a interface apresenta o aviso sem alterar a listagem.
