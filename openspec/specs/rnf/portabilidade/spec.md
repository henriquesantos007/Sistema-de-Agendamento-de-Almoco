# portabilidade Specification

## Purpose
Garantir que o sistema rode em qualquer computador com Python, sem instalação de bibliotecas de terceiros.

## Requirements

### Requirement: NF-POR-01 — Executar apenas com a biblioteca padrão
O sistema DEVE executar em Python 3.10 ou superior, no Windows ou no Linux, sem depender de pacotes de terceiros. O `pytest` é exigido apenas para rodar os testes.

**Prioridade:** Importante
**Casos de uso:** UC05, UC06

#### Scenario: Execução em ambiente limpo
- **GIVEN** um ambiente com Python 3.10 e 0 pacotes de terceiros instalados
- **WHEN** o sistema é executado com `python main.py`
- **THEN** o sistema inicia e exibe "Armazenamento: memoria"
- **AND** 0 erros de importação (`ModuleNotFoundError`) ocorrem
