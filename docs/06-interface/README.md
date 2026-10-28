# Wireframes da Interface

Os wireframes abaixo descrevem a interface web conceitual para os casos de uso
**UC05**, **UC12** e **UC16**, selecionados em
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
