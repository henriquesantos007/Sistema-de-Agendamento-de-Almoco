# usabilidade Specification

## Purpose
Garantir que o usuário saiba, de uma só vez, tudo o que precisa corrigir em um cadastro recusado.

## Requirements

### Requirement: NF-USA-01 — Exibir todos os motivos de recusa de uma vez
O sistema DEVE exibir, em uma única resposta, todos os motivos pelos quais um cadastro foi recusado.

**Prioridade:** Importante
**Casos de uso:** UC05, UC10

#### Scenario: Login e senha inválidos ao mesmo tempo
- **WHEN** o Administrador tenta cadastrar o login "bruno123456789" com a senha "curta"
- **THEN** o sistema exibe 1 única resposta com exatamente 4 motivos: "login deve ter no maximo 12 caracteres", "login nao pode conter numeros", "senha deve ter no minimo 8 caracteres" e "senha deve conter ao menos 3 dos 4 tipos de caracteres: ..."
- **AND** 0 usuários são cadastrados
