# Diagrama de Classes de Domínio

Este diagrama mostra as entidades do sistema, com seus atributos, operações e relacionamentos. Ele organiza o domínio em quatro partes:

- **Usuários:** `Usuario` é uma classe abstrata especializada em `Estudante`, `GestorRestaurante` e `Administrador`. Cada gestor está vinculado ao restaurante que administra.
- **Restaurante e cardápio:** o restaurante mantém seu catálogo de `Prato`s e publica `Cardapio`s **diários** ou **semanais**. Cada `ItemCardapio` representa a oferta de um prato em **uma data específica**, com status próprio. Por isso um prato pode ficar indisponível apenas naquele dia.
- **Pedidos:** o `Pedido` é feito por um estudante para uma data e um restaurante. Seus itens apontam para as ofertas do dia (`ItemCardapio`), e não diretamente para o prato. Isso garante que só se agenda o que foi publicado para aquela data.
- **Pagamento e notificação:** pagamentos via PIX ou cartão passam pelo `GatewayPagamento`, e pagamentos em dinheiro são registrados na retirada. As `Notificacao`s avisam o estudante sobre mudanças no pedido, como o cancelamento por indisponibilidade.

Ao final estão as enumerações, o ciclo de vida do pedido e as formas de pagamento aceitas.

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
classDiagram
    direction TB

    %% ========== USUÁRIOS ==========
    class Usuario {
        <<abstract>>
        -id: Long
        -nome: String
        -email: String
        -senha: String
        -telefone: String
        -dataCadastro: DateTime
        -status: StatusUsuario
        +autenticar(senha: String) boolean
        +atualizarDados(nome: String, telefone: String)
        +alterarSenha(atual: String, nova: String)
        +ativar()
        +desativar()
    }

    class Estudante {
        -matricula: String
    }

    class GestorRestaurante {
    }

    class Administrador {
    }

    Usuario <|-- Estudante
    Usuario <|-- GestorRestaurante
    Usuario <|-- Administrador

    %% ========== RESTAURANTE E CARDÁPIO ==========
    class Restaurante {
        -id: Long
        -nome: String
        -descricao: String
        -localizacao: String
        -telefone: String
        -horarioLimiteAgendamento: Time
        -status: StatusRestaurante
        -dataCadastro: DateTime
        +atualizarDados()
        +cardapioVigenteEm(data: Date) Cardapio
    }

    class Prato {
        -id: Long
        -nome: String
        -descricao: String
        -preco: Decimal
        -imagemUrl: String
        -ativo: boolean
        +atualizar()
    }

    class Cardapio {
        -id: Long
        -tipo: TipoCardapio
        -dataInicio: Date
        -dataFim: Date
        -status: StatusCardapio
        +adicionarItem(prato: Prato, data: Date, quantidadeMaxima: Integer)
        +removerItem(item: ItemCardapio)
        +cobreData(data: Date) boolean
        +itensDoDia(data: Date) List~ItemCardapio~
        +publicar()
        +encerrar()
    }

    class ItemCardapio {
        -id: Long
        -data: Date
        -quantidadeMaxima: Integer
        -quantidadeReservada: int
        -status: StatusItemCardapio
        -motivoIndisponibilidade: String
        +estaDisponivel() boolean
        +reservar(quantidade: int)
        +liberar(quantidade: int)
        +marcarIndisponivel(motivo: String)
    }

    %% ========== PEDIDOS ==========
    class Pedido {
        -id: Long
        -dataCriacao: DateTime
        -dataAgendamento: Date
        -horarioRetirada: Time
        -status: StatusPedido
        -valorTotal: Decimal
        -motivoCancelamento: String
        +adicionarItem(item: ItemCardapio, quantidade: int)
        +removerItem(item: ItemPedido)
        +calcularTotal() Decimal
        +confirmar()
        +cancelar(motivo: String)
        +atualizarStatus(status: StatusPedido)
    }

    class ItemPedido {
        -id: Long
        -quantidade: int
        -precoUnitario: Decimal
        +calcularSubtotal() Decimal
    }

    %% ========== PAGAMENTO ==========
    class Pagamento {
        -id: Long
        -valor: Decimal
        -dataPagamento: DateTime
        -status: StatusPagamento
        -metodo: MetodoPagamento
        +processar()
        +confirmar()
        +estornar()
        +ehOnline() boolean
        +registrarRecebimentoEmDinheiro()
    }

    class GatewayPagamento {
        <<interface>>
        +processarPagamento(pagamento: Pagamento) boolean
        +consultarPagamento(id: Long) StatusPagamento
        +estornarPagamento(id: Long) boolean
    }

    %% ========== NOTIFICAÇÃO ==========
    class Notificacao {
        -id: Long
        -mensagem: String
        -dataEnvio: DateTime
        -lida: boolean
        +marcarComoLida()
    }

    %% ========== RELACIONAMENTOS ==========
    GestorRestaurante "1..*" --> "1" Restaurante : gerencia
    Restaurante "1" *-- "0..*" Prato : oferece
    Restaurante "1" *-- "0..*" Cardapio : publica
    Cardapio "1" *-- "1..*" ItemCardapio : contém
    ItemCardapio "0..*" --> "1" Prato : oferta de

    Estudante "1" -- "0..*" Pedido : realiza
    Pedido "0..*" --> "1" Restaurante : destinado a
    Pedido "1" *-- "1..*" ItemPedido : contém
    ItemPedido "0..*" --> "1" ItemCardapio : refere-se a
    Pedido "1" *-- "0..1" Pagamento : possui
    Pagamento ..> GatewayPagamento : utiliza (PIX/cartão)

    Estudante "1" -- "0..*" Notificacao : recebe
    Notificacao "0..*" --> "0..1" Pedido : sobre

    note for Pedido "dataAgendamento deve estar no período de um cardápio PUBLICADO e respeitar o horário limite"
    note for Pagamento "PIX e CARTAO são processados pelo GatewayPagamento. DINHEIRO fica PENDENTE e é registrado pelo gestor na retirada."
    note for ItemCardapio "Oferta de um prato em uma data específica; pode ficar INDISPONIVEL só naquele dia"
```

## Enumerações

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
classDiagram
    direction LR

    class StatusUsuario {
        <<enumeration>>
        ATIVO
        INATIVO
        BLOQUEADO
    }
    class StatusRestaurante {
        <<enumeration>>
        ATIVO
        INATIVO
        PENDENTE
    }
    class TipoCardapio {
        <<enumeration>>
        DIARIO
        SEMANAL
    }
    class StatusCardapio {
        <<enumeration>>
        RASCUNHO
        PUBLICADO
        ENCERRADO
    }
    class StatusItemCardapio {
        <<enumeration>>
        DISPONIVEL
        ESGOTADO
        INDISPONIVEL
    }
    class StatusPedido {
        <<enumeration>>
        AGUARDANDO_PAGAMENTO
        AGENDADO
        ACEITO
        EM_PREPARO
        PRONTO
        RETIRADO
        RECUSADO
        CANCELADO
    }
    class StatusPagamento {
        <<enumeration>>
        PENDENTE
        APROVADO
        RECUSADO
        CANCELADO
        ESTORNADO
    }
    class MetodoPagamento {
        <<enumeration>>
        PIX
        CARTAO
        DINHEIRO
    }
```

### Ciclo de vida do pedido

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
stateDiagram-v2
    state metodo <<choice>>
    [*] --> metodo : estudante confirma o agendamento
    metodo --> AGUARDANDO_PAGAMENTO : PIX ou cartão
    metodo --> AGENDADO : dinheiro na retirada
    AGUARDANDO_PAGAMENTO --> AGENDADO : gateway aprova o pagamento
    AGUARDANDO_PAGAMENTO --> CANCELADO : prazo expirado
    AGENDADO --> ACEITO : restaurante aceita
    AGENDADO --> RECUSADO : restaurante recusa
    AGENDADO --> CANCELADO : estudante cancela ou item indisponível
    ACEITO --> EM_PREPARO
    ACEITO --> CANCELADO : item indisponível no dia
    EM_PREPARO --> PRONTO
    PRONTO --> RETIRADO : estudante retira (se dinheiro, gestor registra o pagamento)
    RETIRADO --> [*]
    RECUSADO --> [*]
    CANCELADO --> [*]
```

### Formas de pagamento

| Método | Quando é pago | Passa pelo Gateway? | Status do `Pagamento` ao agendar | Se o pedido for cancelado |
|--------|---------------|---------------------|----------------------------------|---------------------------|
| `PIX` | No aplicativo, ao agendar | Sim | `PENDENTE` → `APROVADO` ou `RECUSADO` | Estorno pelo gateway (`ESTORNADO`) |
| `CARTAO` | No aplicativo, ao agendar | Sim | `PENDENTE` → `APROVADO` ou `RECUSADO` | Estorno pelo gateway (`ESTORNADO`) |
| `DINHEIRO` | No restaurante, na retirada | Não | `PENDENTE` até a retirada, quando vira `APROVADO` | Nada a estornar (`CANCELADO`) |
