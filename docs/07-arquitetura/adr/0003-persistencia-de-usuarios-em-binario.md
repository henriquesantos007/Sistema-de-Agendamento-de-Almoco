# ADR-0003: Adotar persistência de usuários em arquivo binário e manter a memória RAM

- Status: Aceito
- Data: 2026-10-07
- Origem: PR 11X, merge `a64dd9c` (`feat(tratamento de erros): implementar validações nos campos de login e senha`)

## Contexto

Até o sprint 1, os usuários eram guardados apenas em memória (`RepositorioUsuariosMemoria`) e os dados se perdiam ao encerrar a execução. O Laboratório 2 exige permitir o armazenamento de usuários também em arquivo binário ou banco de dados, com escolha no início da execução junto ao armazenamento em RAM, e com tratamento de exceções (por exemplo, `IOError` ou `SQLException`). A aplicação já depende somente da abstração `RepositorioUsuarios`, definida no domínio. Além do arquivo binário, foi avaliada uma implementação com SQLite (`RepositorioUsuariosSQLite`, usando o módulo `sqlite3`).

## Decisão

Oferecer somente dois mecanismos de armazenamento, ambos como implementações de `RepositorioUsuarios` na camada de infraestrutura:

- `persistencia/memoria/`: `RepositorioUsuariosMemoria`, já existente desde o sprint 1, mantido como opção padrão.
- `persistencia/arquivo/`: `RepositorioUsuariosArquivo` serializa os usuários com `pickle` em arquivo binário. Herda de `RepositorioUsuariosMemoria` para reaproveitar as consultas, carrega o arquivo ao iniciar e regrava a cada inclusão com escrita atômica (arquivo temporário e `os.replace`), revertendo a memória se a gravação falhar.

Encapsular as falhas de arquivo (`IOError`) e de serialização em `ErroPersistencia`, definida no domínio (`source/dominio/usuarios/excecoes.py`), de modo que aplicação e apresentação não dependam de `pickle` nem de detalhes de infraestrutura.

Escolher o mecanismo no início da execução por `criar_repositorio_usuarios` (`persistencia/fabrica_repositorio.py`), com as opções `memoria` e `arquivo`, expostas no `main.py` por `--armazenamento` e `--caminho`.

Descartar o SQLite: não criar o pacote `persistencia/sqlite/` e remover a opção `sqlite` da fábrica. O enunciado exige arquivo binário *ou* banco de dados, então um dos dois, somado à memória RAM, atende ao requisito, e manter apenas um evita sustentar um segundo mecanismo de persistência que não foi exigido.

## Consequências

- Os dados passam a sobreviver entre execuções.
- `ControladorUsuario` e os validadores não precisam de alteração, pois dependem apenas de `RepositorioUsuarios`.
- Falhas de arquivo têm tratamento único por meio de `ErroPersistencia`, com a causa original em `__cause__`.
- A troca de implementação continua demonstrada pela escolha entre `memoria` e `arquivo`.
- O tratamento de exceções exigido é atendido para `IOError`; não há tratamento de erros de banco de dados, pois o sistema não usa banco.
- Um novo mecanismo, inclusive um banco de dados, pode ser adicionado criando um pacote em `persistencia/` e registrando-o na fábrica; nesse caso, a decisão deve ser registrada em um novo ADR.
- O `pickle` só deve carregar arquivos gerados pela própria aplicação; arquivos gerados antes de mudanças nas classes de domínio ficam incompatíveis e geram `ErroPersistencia`.
- O repositório em arquivo não trata acesso simultâneo de vários processos.
- Os arquivos de dados ficam em `dados/` e não devem ser versionados.

## Alternativas consideradas

- Manter o arquivo binário e também o SQLite; rejeitada porque o enunciado aceita um dos dois e o SQLite acrescentaria um segundo mecanismo a manter sem ser exigido.
- Usar somente SQLite; rejeitada porque o arquivo binário já atende ao requisito e a troca de implementação continua demonstrada entre RAM e arquivo.
- Usar JSON ou CSV; rejeitada porque o enunciado pede arquivo binário.
- Propagar `IOError` até a aplicação; rejeitada por acoplar as camadas superiores à infraestrutura.