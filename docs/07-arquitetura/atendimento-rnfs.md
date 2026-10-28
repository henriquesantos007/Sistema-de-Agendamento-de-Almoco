# Atendimento dos Requisitos Não Funcionais

Esta tabela relaciona cada RNF especificado ao mecanismo da implementação
atual e ao critério que permite verificar seu atendimento. Os limites de tempo
são metas de aceitação; resultados medidos dependem do ambiente e da massa de
dados usados no teste.

| RNF | Como é atendido | Critério de verificação |
|---|---|---|
| [NF-DES-01 — Tempo de cadastro](../../openspec/specs/rnf/desempenho/spec.md) | Repositórios em memória mantêm os registros carregados e a validação executa no fluxo de cadastro; a persistência em arquivo é selecionável. | Cadastrar 1 usuário com 10.000 já existentes em memória e em arquivo; medir com `time.perf_counter`; concluir em até **1 s**. |
| [NF-DES-02 — Tempo de listagem e carga](../../openspec/specs/rnf/desempenho/spec.md) | A listagem consulta a coleção já carregada; o repositório de arquivo carrega a coleção no início da execução. | Obter lista de 10.000 usuários em até **100 ms** e carregar arquivo com 10.000 usuários em até **1 s**, medindo com `time.perf_counter`. |
| [NF-SEG-01 — Não exibir senhas](../../openspec/specs/rnf/seguranca/spec.md) | Listagens apresentam dados de identificação sem senha/hash; mensagens de validação não incluem o valor informado para senha. | Para usuários cadastrados, a listagem contém **0** senhas e **0** ocorrências de `pbkdf2_sha256`; a resposta de validação não contém a senha digitada. |
| [NF-SEG-02 — Armazenar apenas o hash](../../openspec/specs/rnf/seguranca/spec.md) | `gerar_hash_senha` armazena PBKDF2-SHA256 com sal aleatório de 16 bytes e 600.000 iterações. | Verificar que o arquivo contém **0** ocorrências da senha em texto puro e que dois cadastros da mesma senha produzem hashes distintos. |
| [NF-CON-01 — Preservar dados em falha de gravação](../../openspec/specs/rnf/confiabilidade/spec.md) | Repositórios de arquivo gravam em temporário e substituem o destino ao concluir; quando falham, revertem o estado em memória e lançam erro de persistência. | Simular diretório sem permissão: manter o hash do arquivo e a contagem anterior, descartar o registro e exibir uma mensagem de falha sem encerrar inesperadamente. |
| [NF-CON-02 — Recusar arquivo corrompido](../../openspec/specs/rnf/confiabilidade/spec.md) | A carga valida a estrutura e a versão serializada; erros de leitura/decodificação são encapsulados em erro de persistência e tratados na inicialização. | Iniciar com bytes inválidos: exibir uma mensagem iniciada por “Não foi possível iniciar o armazenamento”, sem carregar dados inválidos nem imprimir traceback. |
| [NF-USA-01 — Exibir todos os motivos de recusa](../../openspec/specs/rnf/usabilidade/spec.md) | Validadores acumulam os motivos antes de o controlador recusar o cadastro; a CLI imprime todas as mensagens na mesma resposta. | Informar login e senha inválidos simultaneamente; exibir **1** resposta com todos os **4** motivos especificados e cadastrar **0** usuários. |
| [NF-POR-01 — Executar apenas com a biblioteca padrão](../../openspec/specs/rnf/portabilidade/spec.md) | O código de produção usa a biblioteca padrão do Python; pytest é necessário somente para testes. | Em Windows ou Linux com Python **3.10+** e **0** pacotes externos instalados, executar `python main.py` sem `ModuleNotFoundError`. |
| [NF-MAN-01 — Regras independentes do armazenamento](../../openspec/specs/rnf/manutenibilidade/spec.md) | Aplicação e domínio usam `RepositorioUsuarios` e `RepositorioRestaurantes`; a fábrica de infraestrutura é o ponto único de criação dos repositórios concretos. | Encontrar **0** importações de `source.infraestrutura` em domínio/aplicação e **1** módulo de produção que instancia os repositórios concretos: `fabrica_repositorio.py`. |
| [NF-MAN-02 — Acesso por fachada única](../../openspec/specs/rnf/manutenibilidade/spec.md) | `FacadeSingletonController` encapsula os controladores, impede construção direta e devolve a mesma instância ao cliente no processo de produção. | Repetir `obter_instancia()` e receber a mesma instância; confirmar que a construção direta gera `TypeError` e que `main.py` importa **0** controladores. |

Os requisitos completos, cenários e prioridades estão nas especificações
OpenSpec vinculadas na primeira coluna. Os testes automatizados verificam
comportamentos funcionais e invariantes; os limites temporais de desempenho
devem ser medidos na configuração-alvo com a massa de dados indicada.
