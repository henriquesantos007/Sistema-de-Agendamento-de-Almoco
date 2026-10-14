# Diagramas de Classes de Análise (Fronteira, Controle e Entidade)

Estereótipos utilizados:

| Estereótipo | Papel |
|-------------|-------|
| `<<Boundary>>` (Fronteira) | Interface com um ator: telas e integrações com sistemas externos. |
| `<<Control>>` (Controle) | Coordena um caso de uso e aplica as regras de negócio. |
| `<<Entity>>` (Entidade) | Informação persistente do domínio e as coleções que a armazenam. |

Regras de comunicação respeitadas: **Ator ↔ Fronteira ↔ Controle ↔ Entidade**. Fronteiras não acessam entidades diretamente, e entidades não conhecem fronteiras nem controles.

---

## 1. Gerenciamento de Usuários (Sprint 1)

Cobre os casos de uso **Cadastrar Usuário**, **Cadastrar-se como Estudante** e **Listar Usuários**. Na Sprint 1, `RepositorioUsuarios` guarda os usuários numa coleção em **memória RAM**.

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
classDiagram
    direction TB

    class TelaCadastroUsuario {
        <<Boundary>>
        +exibirFormulario()
        +submeter(dados: DadosUsuario)
        +exibirSucesso(usuario: Usuario)
        +exibirErros(erros: List~String~)
    }

    class TelaListagemUsuarios {
        <<Boundary>>
        +solicitarListagem()
        +exibirUsuarios(usuarios: List~Usuario~)
    }

    class ControladorUsuario {
        <<Control>>
        +cadastrarUsuario(dados: DadosUsuario) Usuario
        +listarUsuarios() List~Usuario~
    }

    class ValidadorUsuario {
        <<Control>>
        +validar(dados: DadosUsuario) List~String~
        -emailEhValido(email: String) boolean
        -emailJaCadastrado(email: String) boolean
        -matriculaJaCadastrada(matricula: String) boolean
    }

    class RepositorioUsuarios {
        <<Entity>>
        -usuarios: List~Usuario~
        -proximoId: Long
        +adicionar(usuario: Usuario) Usuario
        +listarTodos() List~Usuario~
        +buscarPorEmail(email: String) Usuario
        +existeMatricula(matricula: String) boolean
    }

    class Usuario {
        <<Entity>>
        -id: Long
        -nome: String
        -email: String
        -senha: String
        -telefone: String
        -dataCadastro: DateTime
        -status: StatusUsuario
    }

    class Estudante {
        <<Entity>>
        -matricula: String
    }

    class GestorRestaurante {
        <<Entity>>
        -restauranteId: Long
    }

    class Administrador {
        <<Entity>>
    }

    TelaCadastroUsuario --> ControladorUsuario : solicita cadastro
    TelaListagemUsuarios --> ControladorUsuario : solicita listagem
    ControladorUsuario --> ValidadorUsuario : valida dados
    ControladorUsuario --> RepositorioUsuarios : adiciona / lista
    ValidadorUsuario --> RepositorioUsuarios : consulta unicidade
    RepositorioUsuarios o-- "0..*" Usuario : armazena
    Usuario <|-- Estudante
    Usuario <|-- GestorRestaurante
    Usuario <|-- Administrador
```

### Colaboração: Cadastrar Usuário

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
sequenceDiagram
    actor Admin as Administrador
    participant T as TelaCadastroUsuario
    participant C as ControladorUsuario
    participant V as ValidadorUsuario
    participant R as RepositorioUsuarios

    Admin->>T: preenche dados e perfil
    T->>C: cadastrarUsuario(dados)
    C->>V: validar(dados)
    V->>R: buscarPorEmail / existeMatricula
    R-->>V: resultado
    alt dados inválidos
        V-->>C: lista de erros
        C-->>T: erros
        T-->>Admin: exibirErros
    else dados válidos
        V-->>C: sem erros
        C->>C: cria Estudante, Gestor ou Administrador
        C->>R: adicionar(usuario)
        R-->>C: usuario com id
        C-->>T: usuario
        T-->>Admin: exibirSucesso
    end
```

### Colaboração: Listar Usuários

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
sequenceDiagram
    actor Admin as Administrador
    participant T as TelaListagemUsuarios
    participant C as ControladorUsuario
    participant R as RepositorioUsuarios

    Admin->>T: abre a listagem
    T->>C: listarUsuarios()
    C->>R: listarTodos()
    R-->>C: usuarios
    C-->>T: usuarios
    T-->>Admin: exibirUsuarios
```

---

## 2. Cardápio e Agendamento

Cobre **Publicar Cardápio**, **Agendar Almoço**, **Cancelar Agendamento** e **Informar Indisponibilidade no Dia**, incluindo a regra de que só se agenda dentro do período de um cardápio publicado.

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
classDiagram
    direction TB

    class TelaCardapios {
        <<Boundary>>
        +exibirDatasDisponiveis(datas: List~Date~)
        +exibirItensDoDia(itens: List~ItemCardapio~)
    }
    class TelaAgendamento {
        <<Boundary>>
        +selecionarData(data: Date)
        +selecionarItens(itens: List~ItemSelecionado~)
        +confirmar(metodo: MetodoPagamento)
    }
    class TelaMeusPedidos {
        <<Boundary>>
        +exibirPedidos(pedidos: List~Pedido~)
        +solicitarCancelamento(pedido: Pedido)
    }
    class TelaGestaoCardapio {
        <<Boundary>>
        +definirPeriodo(tipo: TipoCardapio, inicio: Date, fim: Date)
        +definirPratosDoDia(data: Date, pratos: List~Prato~)
        +publicar()
        +informarIndisponibilidade(item: ItemCardapio, motivo: String)
    }
    class TelaPedidosDoDia {
        <<Boundary>>
        +exibirPedidos(data: Date, pedidos: List~Pedido~)
        +atualizarStatus(pedido: Pedido, status: StatusPedido)
        +registrarPagamentoEmDinheiro(pedido: Pedido)
    }
    class InterfaceGatewayPagamento {
        <<Boundary>>
        +processar(pagamento: Pagamento) boolean
        +estornar(pagamento: Pagamento) boolean
    }
    class InterfaceNotificacao {
        <<Boundary>>
        +enviar(notificacao: Notificacao)
    }

    class ControladorCardapio {
        <<Control>>
        +publicarCardapio(cardapio: Cardapio)
        +listarDatasDisponiveis(restaurante: Restaurante) List~Date~
        +listarItensDoDia(restaurante: Restaurante, data: Date) List~ItemCardapio~
        +informarIndisponibilidade(item: ItemCardapio, motivo: String)
    }
    class ValidadorJanelaAgendamento {
        <<Control>>
        +dataPermiteAgendamento(restaurante: Restaurante, data: Date) boolean
        +permiteCancelamento(pedido: Pedido) boolean
    }
    class ControladorAgendamento {
        <<Control>>
        +agendar(estudante: Estudante, data: Date, itens: List~ItemSelecionado~) Pedido
        +cancelar(pedido: Pedido)
        +cancelarPedidosAfetados(item: ItemCardapio, motivo: String)
        +listarPedidosDoDia(restaurante: Restaurante, data: Date) List~Pedido~
    }
    class ControladorPagamento {
        <<Control>>
        +pagar(pedido: Pedido, metodo: MetodoPagamento)
        +registrarPagamentoEmDinheiro(pedido: Pedido)
        +estornar(pedido: Pedido)
    }
    class ControladorNotificacao {
        <<Control>>
        +notificarCancelamento(pedido: Pedido, motivo: String)
    }

    class Restaurante { <<Entity>> }
    class Cardapio { <<Entity>> }
    class ItemCardapio { <<Entity>> }
    class Prato { <<Entity>> }
    class Pedido { <<Entity>> }
    class ItemPedido { <<Entity>> }
    class Pagamento { <<Entity>> }
    class Estudante { <<Entity>> }
    class Notificacao { <<Entity>> }

    TelaCardapios --> ControladorCardapio
    TelaGestaoCardapio --> ControladorCardapio
    TelaAgendamento --> ControladorAgendamento
    TelaMeusPedidos --> ControladorAgendamento
    TelaPedidosDoDia --> ControladorAgendamento
    TelaPedidosDoDia --> ControladorPagamento : pagamento em dinheiro

    ControladorCardapio --> ValidadorJanelaAgendamento
    ControladorAgendamento --> ValidadorJanelaAgendamento
    ControladorCardapio --> ControladorAgendamento : cancela afetados
    ControladorAgendamento --> ControladorPagamento
    ControladorAgendamento --> ControladorNotificacao
    ControladorPagamento --> InterfaceGatewayPagamento : só PIX/cartão
    ControladorNotificacao --> InterfaceNotificacao

    ControladorCardapio --> Cardapio
    ControladorCardapio --> ItemCardapio
    ValidadorJanelaAgendamento --> Cardapio
    ValidadorJanelaAgendamento --> Restaurante
    ControladorAgendamento --> Pedido
    ControladorAgendamento --> ItemCardapio
    ControladorPagamento --> Pagamento
    ControladorNotificacao --> Notificacao

    Restaurante "1" *-- "0..*" Cardapio
    Restaurante "1" *-- "0..*" Prato
    Cardapio "1" *-- "1..*" ItemCardapio
    ItemCardapio "0..*" --> "1" Prato
    Estudante "1" -- "0..*" Pedido
    Pedido "1" *-- "1..*" ItemPedido
    ItemPedido "0..*" --> "1" ItemCardapio
    Pedido "1" *-- "0..1" Pagamento
    Estudante "1" -- "0..*" Notificacao
```

> Os atributos e métodos das entidades estão detalhados em [diagrama-de-classes.md](diagrama-de-classes.md).

### Colaboração: Informar Indisponibilidade no Dia

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
sequenceDiagram
    actor G as Gestor de Restaurante
    participant T as TelaGestaoCardapio
    participant CC as ControladorCardapio
    participant CA as ControladorAgendamento
    participant CP as ControladorPagamento
    participant CN as ControladorNotificacao
    participant GW as InterfaceGatewayPagamento

    G->>T: marca item do dia como indisponível (motivo)
    T->>CC: informarIndisponibilidade(item, motivo)
    CC->>CC: item.marcarIndisponivel(motivo)
    CC->>CA: cancelarPedidosAfetados(item, motivo)
    loop para cada pedido da data com o item
        CA->>CA: pedido.cancelar(motivo)
        opt pedido já pago
            CA->>CP: estornar(pedido)
            CP->>GW: estornar(pagamento)
        end
        CA->>CN: notificarCancelamento(pedido, motivo)
    end
    CC-->>T: confirmação
    T-->>G: exibe pedidos cancelados
```
