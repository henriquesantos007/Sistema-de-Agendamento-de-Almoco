# ADR-0004: Remover o pacote de apresentação vazio

- Status: Aceito
- Data: 2026-10-27
- Origem: PR #17, merge `41db3aa` (`Chore(arquitetura): Remove módulo apresentação`)

## Contexto

O ADR-0002 criou o pacote `source/apresentacao/web` para receber a futura interface web. Até a Entrega 1 nenhuma tela foi implementada: a interação com o sistema acontece pelo `main.py`, que lê as opções `--armazenamento` e `--caminho`, cadastra usuários e lista os cadastrados. A avaliação da Entrega 1 apontou o pacote `apresentacao/web` vazio como ponto a melhorar.

## Decisão

Remover os pacotes vazios `source/apresentacao/` e `source/apresentacao/web/`. Enquanto não houver interface gráfica ou web, o `main.py` cumpre o papel de fronteira: monta as dependências (repositório, validadores e controlador) e exibe os resultados, falando apenas com o `ControladorUsuario`.

## Consequências

- A estrutura de pastas passa a refletir apenas o que está implementado: `dominio`, `aplicacao` e `infraestrutura`.
- As classes de fronteira do modelo de análise (`TelaCadastroUsuario` e `TelaListagemUsuarios`) continuam válidas como conceito e hoje são atendidas pelo `main.py`.
- Quando a interface web for implementada, a camada de apresentação deve ser recriada e a decisão registrada em um novo ADR.

## Alternativas consideradas

- Manter o pacote vazio até a interface web; rejeitada porque sugere uma camada que não existe e foi apontada na avaliação.
- Criar agora uma interface web mínima; rejeitada por estar fora do escopo das sprints atuais.
