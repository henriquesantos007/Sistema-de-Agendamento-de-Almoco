# Diagramas de Classes de Análise (Fronteira, Controle e Entidade)

Estereótipos utilizados:

| Estereótipo | Papel |
|-------------|-------|
| `<<Boundary>>` (Fronteira) | Interface com um ator: telas e integrações com sistemas externos. |
| `<<Control>>` (Controle) | Coordena um caso de uso e aplica as regras de negócio. |
| `<<Entity>>` (Entidade) | Informação persistente do domínio e as coleções que a armazenam. |

Regras de comunicação respeitadas: **Ator ↔ Fronteira ↔ Controle ↔ Entidade**. Fronteiras não acessam entidades diretamente, e entidades não conhecem fronteiras nem controles.

---

## 1. Gerenciamento de Usuários (Sprint 1 e Sprint 3)

Cobre os casos de uso **Cadastrar Usuário**, **Cadastrar-se como Estudante**,
**Listar Usuários**, **Editar Usuário**, **Consultar Usuário** e **Remover
Usuário**. O diagrama registra a evolução do repositório em memória da Sprint
1; no Sprint 3, as mesmas operações também são delegadas às implementações de
arquivo por meio do contrato `RepositorioUsuarios`.

As classes de fronteira representam interações conceituais; a interface
executável atual continua sendo a CLI de `main.py`.

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

    class TelaGerenciamentoUsuario {
        <<Boundary>>
        +consultar(usuarioId: int)
        +exibirUsuario(usuario: Usuario)
        +editar(usuarioId: int, dados: DadosUsuario)
        +remover(usuarioId: int)
        +exibirResultado(mensagem: String)
        +exibirErros(erros: List~String~)
    }

    class ControladorUsuario {
        <<Control>>
        +cadastrar(dados: DadosUsuario) Usuario
        +listar_todos() List~Usuario~
        +buscar_por_id(id_usuario: int) Usuario
        +atualizar(id_usuario: int, dados_atualizados: DadosUsuario) Usuario
        +remover(id_usuario: int)
    }

    class ValidadorUsuario {
        <<Control>>
        +validar(dados: DadosUsuario, repositorio: RepositorioUsuarios, id_ignorado: Optional~int~) List~String~
    }

    class RepositorioUsuarios {
        <<Entity>>
        -usuarios: List~Usuario~
        -proximo_id: int
        +adicionar(usuario: Usuario) Usuario
        +listar_todos() List~Usuario~
        +buscar_por_email(email: String) Usuario
        +buscar_por_id(id_usuario: int) Usuario
        +atualizar(usuario_atualizado: Usuario) Usuario
        +remover(id_usuario: int)
        +existe_login(login: String, id_ignorado: Optional~int~) boolean
        +existe_matricula(matricula: String, id_ignorado: Optional~int~) boolean
        +existe_telefone(telefone: String, id_ignorado: Optional~int~) boolean
        +contar() int
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
    TelaGerenciamentoUsuario --> ControladorUsuario : consulta / edita / remove
    ControladorUsuario --> ValidadorUsuario : valida dados
    ControladorUsuario --> RepositorioUsuarios : CRUD / conta
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
    T->>C: cadastrar(dados)
    C->>V: validar(dados, repositorio)
    V->>R: existe_login / buscar_por_email / existe_matricula
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
    T->>C: listar_todos()
    C->>R: listar_todos()
    R-->>C: usuarios
    C-->>T: usuarios
    T-->>Admin: exibirUsuarios
```

### Colaboração: Consultar, editar e remover usuário

```mermaid
%%{init: {"flowchart": {"useMaxWidth": false}, "class": {"useMaxWidth": false}, "sequence": {"useMaxWidth": false}, "state": {"useMaxWidth": false}}}%%
sequenceDiagram
    actor Admin as Administrador
    participant T as TelaGerenciamentoUsuario
    participant C as ControladorUsuario
    participant V as ValidadorUsuario
    participant R as RepositorioUsuarios

    Admin->>T: consulta(usuarioId)
    T->>C: buscar_por_id(usuarioId)
    C->>R: buscar_por_id(usuarioId)
    R-->>C: usuario ou None
    alt usuário não encontrado
        C-->>T: erro de não encontrado
        T-->>Admin: exibe erro
    else usuário encontrado
        C-->>T: usuario
        T-->>Admin: exibe dados sem senha/hash
    end

    Admin->>T: editar(usuarioId, dados)
    T->>C: atualizar(usuarioId, dados)
    C->>R: buscar_por_id(usuarioId)
    R-->>C: usuario existente
    C->>V: validar(dados, repositorio, id_ignorado=usuarioId)
    V->>R: verifica unicidade excluindo o próprio usuário
    R-->>V: resultado
    alt dados inválidos
        V-->>C: motivos de validação
        C-->>T: recusa sem alterar o usuário
    else dados válidos
        C->>R: atualizar(usuario)
        R-->>C: usuario atualizado
        C-->>T: sucesso
    end

    Admin->>T: remover(usuarioId)
    T->>C: remover(usuarioId)
    C->>R: buscar_por_id(usuarioId)
    R-->>C: usuario ou None
    alt usuário não encontrado
        C-->>T: erro de não encontrado
    else usuário encontrado
        C->>R: remover(usuarioId)
        R-->>C: removido
        C-->>T: resultado
    end
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

> Os atributos e métodos das entidades estão detalhados em [08-projeto.md](08-projeto.md).

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
