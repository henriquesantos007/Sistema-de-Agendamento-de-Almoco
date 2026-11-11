# Design: Relatórios de Acesso

## Contexto

O sistema é um monólito modular em camadas, executado pela linha de comando.
Antes desta change, `main.py` escolhia as implementações dos repositórios
pelas funções de módulo `criar_repositorio_usuarios(armazenamento, caminho)` e
`criar_repositorio_restaurantes(armazenamento, caminho)`, de
`fabrica_repositorio.py`, uma fábrica simples que decidia por um `if` sobre
`armazenamento`. Pela
[ADR-0008](../../../docs/07-arquitetura/adr/0008-fachada-singleton-dos-controladores.md),
o `main.py` conhece apenas a fachada, que monta internamente validadores e
controladores. Os controladores dependem dos contratos do domínio, não das
implementações de persistência.

O desenho abaixo está implementado e corresponde ao diagrama "Camadas Business
e Infra (S4.1)" de [08-projeto.md](../../../docs/08-projeto.md). A captura do
evento de acesso e a autenticação não fazem parte dele e não existem no
código.

## Decisões

- **Registro de acesso.** `RegistroAcesso`, no domínio
  (`source/dominio/acessos/`), guarda apenas `usuario_id` e `instante`:
  representa um acesso de um usuário em um instante. É imutável, exige id
  inteiro maior ou igual a 1 e instante com fuso horário, que é convertido para
  UTC; valores inválidos levantam `ValueError`. Login e perfil não são copiados
  para o registro. O evento que cria o registro fica para a change que
  implementar a captura.
- **Repository.** O contrato `RepositorioAcessos`, no domínio, oferece apenas
  `registrar(acesso)` e `listar_todos()`, sem operações de atualização ou
  remoção. `RepositorioAcessosMemoria` guarda os registros em uma lista.
- **Arquivo por acréscimo.** `RepositorioAcessosArquivo` grava um registro por
  linha, em JSON, no formato
  `{"usuario_id": 3, "instante": "2026-11-10T15:34:56+00:00"}`, com o instante
  gravado em UTC, em ISO 8601 e com o deslocamento explícito. `registrar`
  acrescenta uma linha ao fim do arquivo, sem reescrever as anteriores, sob uma
  trava que serializa as gravações das threads do processo; se o arquivo
  terminar sem quebra de linha, por uma escrita interrompida, o novo registro
  começa em nova linha. O arquivo é lido em `listar_todos`, não na construção,
  na ordem das linhas. Falhas de leitura ou gravação e linhas inválidas são
  encapsuladas em `ErroPersistencia` do pacote de acessos, que indica o número
  da linha inválida. Por isso esta classe implementa `RepositorioAcessos`
  diretamente e não herda de `RepositorioAcessosMemoria`, ao contrário dos
  repositórios de usuários e restaurantes, cujas versões em arquivo regravam o
  arquivo binário inteiro a cada alteração. O dado de acesso só cresce e nunca
  é editado; regravar tudo a cada acesso custaria proporcionalmente ao
  histórico.
- **Abstract Factory.** A fábrica simples foi substituída por
  `FabricaRepositorios`, abstrata, com `criar_repositorio_usuarios()`,
  `criar_repositorio_restaurantes()` e `criar_repositorio_acessos()`, e pelas
  fábricas concretas `FabricaRepositoriosMemoria` e
  `FabricaRepositoriosArquivo`, em `fabrica_repositorios.py`. Esta recebe os
  caminhos dos arquivos de usuários, restaurantes e acessos. O caminho de
  acessos vem da opção `--caminho-acessos` do `main.py`, no padrão de
  `--caminho-restaurantes`: sem valor na linha de comando, vale o arquivo padrão
  `dados/acessos.jsonl`, análogo a `dados/usuarios.bin` e
  `dados/restaurantes.bin`, com a extensão do formato de texto por linha. A
  composição escolhe a fábrica concreta a partir de `--armazenamento` em um
  único ponto, `escolher_fabrica`. As funções de `fabrica_repositorio.py` e
  seus testes foram removidos. Decisão registrada na
  [ADR-0009](../../../docs/07-arquitetura/adr/0009-repository-e-factory-para-entidades-persistidas.md).
- **Template Method.** `TemplateRelatorioAcesso`, na aplicação
  (`source/aplicacao/relatorios/`), é instanciado com `RepositorioAcessos` e
  `RepositorioUsuarios`. Seu método `gerar()` chama `obter_estatisticas()`,
  comum a todos os formatos, e `formatar(estatisticas)`, especializado por
  `RelatorioAcessoHTML` e `RelatorioAcessoCSV`. Decisão registrada na
  [ADR-0011](../../../docs/07-arquitetura/adr/0011-template-method-para-relatorios-de-acesso.md).
- **Dados do relatório.** `obter_estatisticas()` lê todos os registros, sem
  filtro de período, e produz um `EstatisticasAcesso` com `total_acessos`,
  `usuarios_distintos` e `detalhamento`, uma tupla de `AcessosPorUsuario`
  (`usuario_id`, `login`, `perfil`, `quantidade`). O detalhamento é ordenado
  pela quantidade de acessos, decrescente, e, no empate, por `usuario_id`,
  crescente. Login e perfil são consultados em
  `RepositorioUsuarios.buscar_por_id`; quando o usuário foi removido e a
  consulta devolve `None`, a linha mantém o id e indica login e perfil como
  "usuário removido", e os registros continuam contando nos totais (RF16).
  Senha e e-mail nunca são lidos para o relatório.
- **Documento.** `formatar` produz um `Documento`, com o formato em minúsculas
  (`html` ou `csv`) e o conteúdo textual gerado. O CSV tem dois blocos
  separados por uma linha em branco: o resumo, com cabeçalho
  `total_acessos,usuarios_distintos`, e o detalhamento, com cabeçalho
  `usuario_id,login,perfil,quantidade`. No CSV, login ou perfil iniciados por
  `=`, `+`, `-`, `@`, tabulação ou retorno de carro recebem um apóstrofo na
  frente, para que planilhas não os interpretem como fórmula. O HTML tem as
  tabelas `resumo` e `detalhamento`, com o texto escapado. Os dois formatos
  partem do mesmo `EstatisticasAcesso`, o que garante os mesmos números e a
  mesma ordem (RF17); o texto de login e perfil só difere pelo apóstrofo nos
  casos acima.
- **Serviço.** `ServicoRelatorioAcesso` guarda os repositórios de acessos e de
  usuários e o `LoggerAplicacao`. Em `gerar(formato)`, aceita o formato sem
  diferenciar maiúsculas e com espaços nas pontas, escolhe
  `RelatorioAcessoHTML` ou `RelatorioAcessoCSV`, instancia a subclasse com os
  dois repositórios e chama `gerar()`.
- **Recusa de formato.** Para formato diferente de HTML e CSV, o serviço lança
  `FormatoRelatorioInvalido`, subclasse de `ValueError` definida no pacote de
  aplicação dos relatórios, com a lista de formatos aceitos na mensagem. É a
  mesma convenção de `DadosUsuarioInvalidos` e `DadosRestauranteInvalidos`: o
  controlador ou serviço lança, a fachada repassa sem tratar e o `main.py`
  captura e exibe a mensagem. Nenhum documento é gerado.
- **Adapter de logging.** O contrato `LoggerAplicacao`, definido na aplicação,
  oferece `registrar(evento, detalhes, nivel)`, em que `nivel` é um
  `NivelEvento` opcional (`INFORMACAO`, o padrão, `AVISO` ou `ERRO`).
  `AdaptadorLogging`, em `source/infraestrutura/logs/`, implementa esse
  contrato, converte o nível para `INFO`, `WARNING` ou `ERROR` e delega ao
  módulo `logging` da biblioteca padrão; `criar_adaptador_logging()` configura
  a saída e devolve o Adapter. O serviço registra a geração como informação,
  apenas com o formato normalizado; a recusa como aviso, sem o formato
  digitado, que é entrada livre; e a falha de persistência como erro, repassando
  a exceção. As mensagens não incluem dados pessoais, e os logs não são fonte
  das estatísticas. Decisão registrada na
  [ADR-0010](../../../docs/07-arquitetura/adr/0010-adapter-para-logging.md).
- **Fachada e composição.** O relatório passa pela fachada, como as demais
  operações (ADR-0008). `obter_instancia` recebe também `repositorio_acessos` e
  `logger`; a primeira chamada exige os três repositórios e o logger, e
  chamadas posteriores não podem trocá-los. A fachada monta internamente o
  `ServicoRelatorioAcesso` e expõe `gerar_relatorio_acessos(formato)`, que
  delega ao serviço. A composição em `main.py` escolhe a fábrica concreta,
  obtém dela os três repositórios, cria o `AdaptadorLogging` e entrega tudo a
  `obter_instancia`. O `main.py` não cria nem chama o serviço diretamente; ele
  demonstra o relatório em CSV e HTML e a recusa de um formato não suportado.
- **Perfil do solicitante.** O perfil de quem pede o relatório não é
  verificado: o projeto não tem autenticação, e a restrição ao Administrador
  descrita na spec continua sendo premissa.
- **Resumo de entidades.** Os registros de acesso não entram em
  `obter_contagem_por_entidade` nem em `contar_total_entidades`. São eventos,
  não entidades cadastradas, e somá-los faria o total de entidades crescer a
  cada acesso. O RF12 define o total como a soma de usuários e restaurantes
  cadastrados e continua inalterado. A orientação da ADR-0008 de incluir novas
  entidades nessa contagem vale para entidades cadastradas, o que não é o caso
  dos registros de acesso.

## Alternativas consideradas

- **Copiar login e perfil para o `RegistroAcesso`:** rejeitada para não
  duplicar dados do usuário; o relatório os consulta em `RepositorioUsuarios`.
- **Excluir do relatório os registros de usuários removidos:** rejeitada
  porque o total de acessos deixaria de refletir os acessos ocorridos.
- **Calcular as estatísticas a partir dos logs:** rejeitada pela ADR-0010;
  logs operacionais não são armazenamento estruturado e consultável.
- **Reaproveitar a regravação total em binário das ADR-0003 e ADR-0006 para os
  acessos:** rejeitada pela ADR-0009; o custo de cada registro cresceria com o
  histórico.
- **Manter as funções de módulo da fábrica:** rejeitada pela ADR-0009; são uma
  fábrica simples, não Factory Method nem Abstract Factory.
- **Strategy por formato:** não adotada pela ADR-0011.
- **`main.py` montar e chamar o serviço de relatórios:** rejeitada por
  contornar a fachada, contra a ADR-0008.
- **Incluir os registros de acesso no resumo de entidades:** rejeitada porque
  o total de entidades passaria a crescer a cada acesso e deixaria de ser a
  soma de usuários e restaurantes cadastrados exigida pelo RF12.

## Riscos e limitações conhecidas

- A captura não foi implementada: nenhum registro é criado em execução normal
  e o relatório apresenta totais zero.
- Login e perfil são resolvidos pelo id no momento do relatório. Isso depende
  de os identificadores de usuário não serem reaproveitados durante a vida do
  armazenamento de acessos e de os armazenamentos de usuários e de acessos
  serem usados sempre em conjunto. Recriar ou trocar o armazenamento de
  usuários mantendo o de acessos atribuiria acessos antigos a outro usuário.
  O arquivo de usuários guarda o próximo id e não o reaproveita; o Abstract
  Factory evita combinar mecanismos diferentes na mesma execução, mas não
  impede apagar só o arquivo de usuários.
- A trava de `RepositorioAcessosArquivo` protege apenas threads do mesmo
  processo. Processos diferentes gravando o mesmo arquivo continuam sem
  proteção, coerente com a ADR-0008, segundo a qual os repositórios não tratam
  acesso simultâneo.
- Uma linha truncada por escrita interrompida continua inválida: o registro
  seguinte é gravado em nova linha, mas a leitura falha com `ErroPersistencia`
  indicando a linha truncada até que ela seja corrigida.
- Um arquivo de acessos com BOM ou com linha em branco também é tratado como
  inválido na leitura.
- `criar_adaptador_logging` não desliga a propagação do logger da aplicação
  para o logger raiz; se o raiz também for configurado, os eventos aparecem
  duplicados.
- A consulta de login e perfil faz uma busca por usuário distinto; o volume
  esperado no projeto não justifica outra estratégia agora.
