# Tarefas

- [x] Criar a hierarquia `FabricaRepositorios`, `FabricaRepositoriosMemoria`
  e `FabricaRepositoriosArquivo` para usuários e restaurantes, migrar `main.py`
  e os testes existentes de `fabrica_repositorio.py` para ela e remover as
  funções de módulo (`refactor(persistencia)`).
- [x] Criar a entidade `RegistroAcesso` (`usuario_id`, `instante`) e o
  contrato `RepositorioAcessos` (`registrar`, `listar_todos`, sem atualizar
  nem remover) no domínio (`feat(acessos)`).
- [x] Implementar e testar `RepositorioAcessosMemoria` (`feat(acessos)`).
- [x] Implementar e testar `RepositorioAcessosArquivo`, que implementa o
  contrato diretamente e acrescenta uma linha JSON por registro, com o
  instante em UTC (ISO 8601 com deslocamento), sem reescrever as anteriores,
  encapsulando falhas em `ErroPersistencia` (`feat(acessos)`).
- [x] Adicionar `criar_repositorio_acessos()` às fábricas concretas, com o
  caminho de acessos em `FabricaRepositoriosArquivo`, e testar
  (`feat(acessos)`).
- [x] Criar `EstatisticasAcesso`, `AcessosPorUsuario` e
  `TemplateRelatorioAcesso.obter_estatisticas`, consultando
  `RepositorioAcessos` e `RepositorioUsuarios`, com testes dos cenários de
  RF16, incluindo ordem e empate, usuário removido e ausência de registros
  (`feat(relatorios)`).
- [x] Implementar `RelatorioAcessoHTML` e `RelatorioAcessoCSV` e testar que os
  dois formatos apresentam os mesmos dados na mesma ordem (RF17)
  (`feat(relatorios)`).
- [x] Definir o contrato `LoggerAplicacao` e implementar `AdaptadorLogging`
  sobre o módulo `logging`, com testes que verifiquem a ausência de dados
  pessoais nas mensagens (`feat(logging)`).
- [x] Criar `ServicoRelatorioAcesso.gerar(formato)`, que instancia a subclasse
  do formato com os repositórios e registra o resultado no logger, e
  `FormatoRelatorioInvalido`, com teste da recusa de formato não suportado
  (`feat(relatorios)`).
- [x] Estender `FacadeSingletonController.obter_instancia` com
  `repositorio_acessos` e `logger`, montar o serviço na fachada e expor
  `gerar_relatorio_acessos(formato)`, mantendo os registros de acesso fora
  de `obter_contagem_por_entidade` e `contar_total_entidades` e ajustando os
  testes da fachada (`feat(fachada)`).
- [x] Compor em `main.py` a fábrica concreta escolhida pelo armazenamento, a
  opção `--caminho-acessos` (padrão `dados/acessos.jsonl`) e o
  `AdaptadorLogging`, entregando-os à fachada, e exibir a recusa de formato
  como as demais recusas de validação (`feat(cli)`).
- [x] Proteger as gravações simultâneas de threads e a escrita após linha
  truncada no arquivo de acessos, e neutralizar fórmulas no CSV
  (`fix(acessos)`).
- [x] Atualizar `08-projeto.md`, a tabela de padrões, os casos de uso e o
  status das ADR-0009, ADR-0010 e ADR-0011 conforme o que for implementado
  (`docs`).
