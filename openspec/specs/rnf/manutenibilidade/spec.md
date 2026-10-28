# manutenibilidade Specification

## Purpose
Garantir que os mecanismos de armazenamento (memória e arquivo binário) possam ser trocados ou acrescentados sem alterar as regras de negócio, e que os clientes acessem os controladores por um único ponto.

## Requirements

### Requirement: NF-MAN-01 — Regras de negócio independentes do armazenamento
As camadas de domínio e de aplicação NÃO DEVEM importar módulos da camada de infraestrutura; elas dependem apenas da abstração `RepositorioUsuarios`.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC06, UC12, UC14

#### Scenario: Nenhuma importação de infraestrutura
- **WHEN** se procura por importações de `source.infraestrutura` dentro de `source/dominio/` e `source/aplicacao/`
- **THEN** são encontradas 0 importações

#### Scenario: Escolha do armazenamento em um único ponto
- **WHEN** se procura onde as classes `RepositorioUsuariosMemoria`, `RepositorioUsuariosArquivo`, `RepositorioRestaurantesMemoria` e `RepositorioRestaurantesArquivo` são instanciadas no código de produção
- **THEN** todas são instanciadas em 1 único módulo: `source/infraestrutura/persistencia/fabrica_repositorio.py`

### Requirement: NF-MAN-02 — Acesso aos controladores por uma fachada única
O sistema DEVE expor as operações de usuários e de restaurantes por uma única fachada (`FacadeSingletonController`), com exatamente 1 instância por execução, e os controladores NÃO DEVEM ser instanciados fora dela.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC06, UC12, UC13, UC14, UC15, UC16, UC17

#### Scenario: Mesma instância em todas as chamadas
- **GIVEN** a fachada foi obtida com `obter_instancia(repositorio_usuarios, repositorio_restaurantes)`
- **WHEN** `obter_instancia()` é chamado de novo, sem argumentos
- **THEN** o mesmo objeto é devolvido, e o sistema exibe "Mesma instância da fachada: True"

#### Scenario: Construtor direto bloqueado
- **WHEN** se tenta criar a fachada com `FacadeSingletonController()`
- **THEN** ocorre 1 `TypeError` com a mensagem "Use FacadeSingletonController.obter_instancia(...) em vez de instanciar diretamente."

#### Scenario: Controladores encapsulados na fachada
- **WHEN** se procura onde `ControladorUsuario` e `ControladorRestaurante` são instanciados no código de produção
- **THEN** existe exatamente 1 ponto: `source/aplicacao/fachada/facade_singleton_controller.py`
- **AND** o `main.py` importa 0 controladores
