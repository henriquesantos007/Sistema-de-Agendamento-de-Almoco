# ADR-0003: Adotar persistência de usuários em arquivo binário e SQLite

- Status: Aceito
- Data: 2026-10-07
- Origem: PR 11X, merge `a64dd9c` (`feat(tratamento de erros): implementar validações nos campos de login e senha`)

## Contexto

Até o sprint 1, os usuários eram guardados apenas em memória (`RepositorioUsuariosMemoria`) e os dados se perdiam ao encerrar a execução. O Laboratório 2 exige permitir o armazenamento de usuários também em arquivo binário ou banco de dados, com escolha no início da execução junto ao armazenamento em RAM, e com tratamento de exceções (por exemplo, `IOError` ou `SQLException`). A aplicação já depende somente da abstração `RepositorioUsuarios`, definida no domínio.

## Decisão

Criar duas implementações de `RepositorioUsuarios` na camada de infraestrutura, cada uma em seu pacote, no mesmo padrão de `persistencia/memoria/`:

- `persistencia/arquivo/`: `RepositorioUsuariosArquivo` serializa os usuários com `pickle` em arquivo binário. Herda de `RepositorioUsuariosMemoria` para reaproveitar as consultas, carrega o arquivo ao iniciar e regrava a cada inclusão com escrita atômica (arquivo temporário e `os.replace`), revertendo a memória se a gravação falhar.
- `persistencia/sqlite/`: `RepositorioUsuariosSQLite` usa o módulo `sqlite3` da biblioteca padrão, com tabela única `usuarios` e commit/rollback por operação.

Encapsular as falhas técnicas (`IOError` e `sqlite3.Error`) em `ErroPersistencia`, definida no domínio (`source/dominio/usuarios/excecoes.py`), de modo que aplicação e apresentação não dependam de `pickle` nem de `sqlite3`.

Escolher o mecanismo no início da execução por `criar_repositorio_usuarios` (`persistencia/fabrica_repositorio.py`), com as opções `memoria`, `arquivo` e `sqlite`, expostas no `main.py` por `--armazenamento` e `--caminho`.

## Consequências

- Os dados passam a sobreviver entre execuções.
- `ControladorUsuario` e os validadores não precisam de alteração, pois dependem apenas de `RepositorioUsuarios`.
- Falhas de arquivo e de banco têm tratamento único por meio de `ErroPersistencia`, com a causa original em `__cause__`.
- Novos mecanismos de persistência são adicionados criando um pacote em `persistencia/` e registrando-o na fábrica.
- O `pickle` só deve carregar arquivos gerados pela própria aplicação; arquivos gerados antes de mudanças nas classes de domínio ficam incompatíveis e geram `ErroPersistencia`.
- O repositório em arquivo não trata acesso simultâneo de vários processos.
- Não há restrições `UNIQUE` no banco; a unicidade de e-mail, matrícula e telefone continua garantida apenas pelos validadores.
- Os arquivos de dados ficam em `dados/` e não devem ser versionados.

## Alternativas consideradas

- Usar somente SQLite; rejeitada por não demonstrar a troca de implementação sem alterar a aplicação, e porque o enunciado cita arquivo binário e banco de dados como opções.
- Usar JSON ou CSV; rejeitada porque o enunciado pede arquivo binário.
- Propagar `IOError` e `sqlite3.Error` até a aplicação; rejeitada por acoplar as camadas superiores à infraestrutura.