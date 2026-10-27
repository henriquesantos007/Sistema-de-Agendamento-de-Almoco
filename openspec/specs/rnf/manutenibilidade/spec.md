# manutenibilidade Specification

## Purpose
Garantir que os mecanismos de armazenamento (memória e arquivo binário) possam ser trocados ou acrescentados sem alterar as regras de negócio.

## Requirements

### Requirement: NF-MAN-01 — Regras de negócio independentes do armazenamento
As camadas de domínio e de aplicação NÃO DEVEM importar módulos da camada de infraestrutura; elas dependem apenas da abstração `RepositorioUsuarios`.

**Prioridade:** Essencial
**Casos de uso:** UC05, UC06

#### Scenario: Nenhuma importação de infraestrutura
- **WHEN** se procura por importações de `source.infraestrutura` dentro de `source/dominio/` e `source/aplicacao/`
- **THEN** são encontradas 0 importações

#### Scenario: Escolha do armazenamento em um único ponto
- **WHEN** se procura onde as classes `RepositorioUsuariosMemoria` e `RepositorioUsuariosArquivo` são instanciadas no código de produção
- **THEN** existe exatamente 1 ponto: a função `criar_repositorio_usuarios`, em `source/infraestrutura/persistencia/fabrica_repositorio.py`
