# Diagramas de Casos de Uso

> Convenção de leitura (o Mermaid não tem notação nativa de casos de uso):
> - **Retângulos** são atores; **elipses** (formato arredondado) são casos de uso.
> - Seta contínua (`──►`): associação ator ↔ caso de uso.
> - Seta tracejada com `«include»`: o caso de uso de origem **sempre** executa o de destino.
> - Seta tracejada com `«extend»`: o caso de uso de origem **pode** estender o de destino sob uma condição.

Perfis de usuário do sistema:

| Ator | Descrição |
|------|-----------|
| **Estudante** | Aluno do CI que consulta cardápios e agenda almoços. Faz o próprio cadastro (com matrícula). |
| **Gestor de Restaurante** | Funcionário/responsável de um restaurante parceiro. Publica cardápios e gerencia os pedidos. É cadastrado por um administrador. |
| **Administrador** | Mantém usuários e restaurantes do sistema. |
| **Gateway de Pagamento** | Sistema externo que processa e estorna os pagamentos feitos pelo aplicativo (PIX ou cartão). Não participa do gerenciamento de usuários, por isso só aparece na visão geral. |

---

## 1. Gerenciamento de Usuários (Laboratório 1)

Casos de uso marcados com ⭐ fazem parte da **Sprint 1** (adição e listagem de usuários).

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
flowchart LR
    estudante["🧑‍🎓 Estudante"]
    gestor["🧑‍🍳 Gestor de Restaurante"]
    admin["🛡️ Administrador"]

    subgraph sistema["Sistema de Agendamento de Almoços — Gerenciamento de Usuários"]
        UC01(["Cadastrar-se como Estudante"])
        UC02(["Autenticar-se"])
        UC03(["Editar Perfil"])
        UC04(["Alterar Senha"])
        UC05(["⭐ Cadastrar Usuário"])
        UC06(["⭐ Listar Usuários"])
        UC07(["Filtrar Usuários por Perfil/Status"])
        UC08(["Editar Usuário"])
        UC09(["Ativar/Desativar Usuário"])
        UC10(["Validar Dados do Usuário"])
        UC11(["Vincular Gestor a Restaurante"])
    end

    estudante --> UC01
    estudante --> UC02
    estudante --> UC03
    estudante --> UC04

    gestor --> UC02
    gestor --> UC03
    gestor --> UC04

    admin --> UC02
    admin --> UC05
    admin --> UC06
    admin --> UC08
    admin --> UC09

    UC01 -. "«include»" .-> UC10
    UC05 -. "«include»" .-> UC10
    UC08 -. "«include»" .-> UC10
    UC11 -. "«extend»<br/>(perfil = Gestor)" .-> UC05
    UC07 -. "«extend»" .-> UC06
    UC09 -. "«extend»" .-> UC06
```

| Caso de uso | Resumo |
|-------------|--------|
| **Cadastrar-se como Estudante** | Estudante informa nome, e-mail, telefone e senha. Conta criada com status `ATIVO`. |
| ⭐ **Cadastrar Usuário** | Administrador cadastra usuário de qualquer perfil (Estudante, Gestor de Restaurante ou Administrador). Se for Gestor, vincula-o a um restaurante. |
| ⭐ **Listar Usuários** | Administrador visualiza todos os usuários cadastrados (nome, e-mail, perfil, status). Pode filtrar e, a partir da lista, ativar/desativar. |
| **Validar Dados do Usuário** | Verifica campos obrigatórios, formato de e-mail, e-mail único e telefone único (Estudante). |

---

## 2. Visão Geral do Sistema

A principal regra de negócio está no fluxo de agendamento: **o estudante só agenda para datas cobertas por um cardápio publicado** (diário ou semanal), e o restaurante pode **informar indisponibilidade no próprio dia**, o que cancela os agendamentos afetados e notifica os estudantes. 

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
flowchart LR
    estudante["🧑‍🎓 Estudante"]
    gestor["🧑‍🍳 Gestor de Restaurante"]
    admin["🛡️ Administrador"]
    gateway["💳 Gateway de Pagamento"]

    subgraph sistema["Sistema de Agendamento de Almoços"]

        subgraph acesso["Acesso"]
            UC_Cadastro(["Cadastrar-se"])
            UC_Login(["Autenticar-se"])
        end

        subgraph estudanteUC["Estudante"]
            UC_ConsultarCardapio(["Consultar Cardápios Publicados<br/>(dia/semana)"])
            UC_DetalhesPrato(["Visualizar Detalhes do Prato"])
            UC_Agendar(["Agendar Almoço"])
            UC_SelecionarData(["Selecionar Data Disponível"])
            UC_EscolherPratos(["Escolher Pratos e Quantidades"])
            UC_Pagar(["Realizar Pagamento"])
            UC_Acompanhar(["Acompanhar Pedido"])
            UC_Cancelar(["Cancelar Agendamento"])
            UC_Historico(["Consultar Histórico"])
            UC_Notificacoes(["Visualizar Notificações"])
        end

        subgraph restauranteUC["Gestor de Restaurante"]
            UC_DadosRest(["Gerenciar Dados do Restaurante"])
            UC_Pratos(["Gerenciar Pratos"])
            UC_Publicar(["Publicar Cardápio<br/>(diário ou semanal)"])
            UC_Periodo(["Definir Período e Pratos por Dia"])
            UC_Indisponivel(["Informar Indisponibilidade no Dia"])
            UC_CancelarAfetados(["Cancelar Agendamentos Afetados"])
            UC_Notificar(["Notificar Estudantes"])
            UC_PedidosDia(["Visualizar Agendamentos do Dia"])
            UC_Status(["Atualizar Status do Pedido"])
            UC_Pagamentos(["Consultar Pagamentos"])
            UC_Dinheiro(["Registrar Pagamento em Dinheiro"])
        end

        subgraph adminUC["Administrador"]
            UC_Usuarios(["Gerenciar Usuários"])
            UC_Restaurantes(["Gerenciar Restaurantes"])
            UC_Relatorios(["Consultar Relatórios"])
        end

        subgraph pagamentoUC["Pagamento"]
            UC_Processar(["Processar Pagamento"])
            UC_Estornar(["Estornar Pagamento"])
        end
    end

    %% Estudante
    estudante --> UC_Cadastro
    estudante --> UC_Login
    estudante --> UC_ConsultarCardapio
    estudante --> UC_Agendar
    estudante --> UC_Acompanhar
    estudante --> UC_Historico
    estudante --> UC_Notificacoes

    UC_DetalhesPrato -. "«extend»" .-> UC_ConsultarCardapio
    UC_Agendar -. "«include»" .-> UC_SelecionarData
    UC_Agendar -. "«include»" .-> UC_EscolherPratos
    UC_Agendar -. "«include»" .-> UC_Pagar
    UC_Cancelar -. "«extend»<br/>(antes do horário limite)" .-> UC_Acompanhar

    %% Gestor de Restaurante
    gestor --> UC_Login
    gestor --> UC_DadosRest
    gestor --> UC_Pratos
    gestor --> UC_Publicar
    gestor --> UC_Indisponivel
    gestor --> UC_PedidosDia
    gestor --> UC_Pagamentos

    UC_Publicar -. "«include»" .-> UC_Periodo
    UC_Indisponivel -. "«include»" .-> UC_CancelarAfetados
    UC_CancelarAfetados -. "«include»" .-> UC_Notificar
    UC_Status -. "«extend»" .-> UC_PedidosDia
    UC_Dinheiro -. "«extend»<br/>(retirada paga em dinheiro)" .-> UC_Status

    %% Administrador
    admin --> UC_Login
    admin --> UC_Usuarios
    admin --> UC_Restaurantes
    admin --> UC_Relatorios

    %% Pagamento
    UC_Pagar -. "«include»<br/>(PIX ou cartão)" .-> UC_Processar
    UC_CancelarAfetados -. "«include»<br/>(se já pago)" .-> UC_Estornar
    UC_Cancelar -. "«include»<br/>(se já pago)" .-> UC_Estornar
    UC_Processar --> gateway
    UC_Estornar --> gateway
```

### Descrição dos casos de uso ligados às regras de agendamento

#### Publicar Cardápio (diário ou semanal)
- **Ator:** Gestor de Restaurante
- **Pré-condição:** gestor autenticado; restaurante `ATIVO`; pratos cadastrados.
- **Fluxo principal:**
  1. Gestor escolhe o tipo de cardápio: **diário** (uma data) ou **semanal** (intervalo de datas).
  2. Para cada dia do período, seleciona os pratos oferecidos e, opcionalmente, a quantidade máxima.
  3. Sistema valida que não há outro cardápio publicado sobrepondo as mesmas datas.
  4. Gestor publica. O cardápio passa a `PUBLICADO` e as datas ficam disponíveis para agendamento.
- **Pós-condição:** estudantes conseguem agendar para as datas do período.

#### Agendar Almoço
- **Ator:** Estudante
- **Pré-condição:** estudante autenticado; existe cardápio `PUBLICADO` cobrindo ao menos uma data futura (ou a data de hoje antes do horário limite).
- **Fluxo principal:**
  1. Estudante escolhe o restaurante.
  2. Sistema exibe **somente** as datas cobertas pelo cardápio publicado e ainda dentro da janela de agendamento.
  3. Estudante escolhe a data e os pratos disponíveis naquele dia, com quantidades.
  4. Estudante seleciona a forma de pagamento (PIX, cartão ou dinheiro na retirada) e confirma.
  5. Sistema reserva as quantidades e registra o pedido para aquela data.
  6. Para PIX ou cartão, o pagamento é enviado ao Gateway de Pagamento; quando aprovado, o pedido passa a `AGENDADO`.
- **Fluxos alternativos:**
  - *2a.* Não há cardápio publicado → sistema informa que ainda não há datas disponíveis.
  - *3a.* Prato esgotado/indisponível na data → não pode ser selecionado.
  - *4a.* Estudante escolhe **dinheiro**: o pedido passa direto a `AGENDADO`, sem passar pelo gateway, com pagamento `PENDENTE`. O gestor registra o recebimento no momento da retirada.
  - *6a.* Pagamento recusado → pedido permanece `AGUARDANDO_PAGAMENTO` e as reservas são liberadas após o prazo.

#### Informar Indisponibilidade no Dia
- **Ator:** Gestor de Restaurante
- **Pré-condição:** cardápio `PUBLICADO` cobrindo a data.
- **Fluxo principal:**
  1. Gestor seleciona a data e marca um prato (ou o dia inteiro) como indisponível, informando o motivo.
  2. Sistema identifica os pedidos daquela data que contêm os itens afetados e ainda não foram finalizados.
  3. Sistema cancela esses pedidos com o motivo informado e solicita estorno dos que já foram pagos.
  4. Sistema notifica cada estudante afetado.
- **Pós-condição:** itens ficam `INDISPONIVEL`; novos agendamentos para eles são bloqueados.
