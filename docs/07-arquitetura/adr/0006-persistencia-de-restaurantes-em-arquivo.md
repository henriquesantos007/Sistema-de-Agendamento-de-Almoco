# ADR-0006: Persistir restaurantes em arquivo binário

- Status: Aceito
- Data: 2026-10-27

## Contexto

O CRUD de restaurantes inicialmente usa `RepositorioRestaurantesMemoria`, que
perde os registros ao encerrar a execução. O projeto já oferece arquivo binário
com `pickle` para usuários, além de escolha do mecanismo por fábrica.

## Decisão

Oferecer `RepositorioRestaurantesArquivo`, que herda do repositório em memória,
carrega `dados/restaurantes.bin` ao iniciar e grava as alterações com arquivo
temporário e `os.replace`. A fábrica disponibiliza
`criar_repositorio_restaurantes`, com as opções `memoria` e `arquivo`, e permite
informar um caminho alternativo. Falhas de leitura, gravação e serialização
geram `ErroPersistencia` definido no domínio de restaurantes.

## Consequências

- Os restaurantes persistem entre execuções sem alterar a interface de domínio
  ou o controlador.
- O repositório reverte seu estado em memória quando a gravação falha.
- O arquivo usa `pickle` e deve ser tratado como dado confiável, gerado pela
  própria aplicação.
- O armazenamento de restaurantes é independente do arquivo de usuários.
