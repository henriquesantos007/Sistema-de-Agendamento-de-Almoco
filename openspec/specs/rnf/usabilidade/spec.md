# usabilidade Specification

## Purpose
Garantir que o usuário saiba, de uma só vez, tudo o que precisa corrigir em um cadastro ou atualização recusados.

## Requirements

### Requirement: NF-USA-01 — Exibir todos os motivos de recusa de uma vez
O sistema DEVE exibir, em uma única resposta, todos os motivos que levaram à recusa de um cadastro ou de uma atualização.

**Prioridade:** Importante
**Casos de uso:** UC05, UC08, UC10

#### Scenario: Login e senha inválidos ao mesmo tempo
- **WHEN** o Administrador tenta cadastrar o login "bruno123456789" com a senha "curta"
- **THEN** o sistema exibe 1 única resposta com exatamente 4 motivos: "login deve ter no maximo 12 caracteres", "login nao pode conter numeros", "senha deve ter no minimo 8 caracteres" e "senha deve conter ao menos 3 dos 4 tipos de caracteres: ..."
- **AND** 0 usuários são cadastrados

#### Scenario: Atualização inválida exibe todos os motivos e preserva o usuário
- **GIVEN** existem os usuários de ids 1 e 2, e o e-mail do usuário 2 é "ana@ci.ufpb.br"
- **WHEN** o Administrador atualiza o usuário 1 com login "bruno123456789", e-mail "ana@ci.ufpb.br" e senha "curta"
- **THEN** o sistema exibe em uma única mensagem os 5 motivos: "login deve ter no maximo 12 caracteres", "login nao pode conter numeros", "e-mail ja cadastrado", "senha deve ter no minimo 8 caracteres" e "senha deve conter ao menos 3 dos 4 tipos de caracteres: maiusculas, minusculas, numeros e especiais (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ')"
- **AND** os dados do usuário 1 permanecem inalterados
