# Relatório de Elicitação de Requisitos

Abaixo estão detalhadas as técnicas utilizadas pela equipe para levantar e compreender as necessidades do Sistema de Agendamento de Almoço do CI.

## Técnica 1: Análise de Documentos (Histórico de Comunicação)

- **Data:** 08/10/2026
- **Local:** Ambiente Virtual (Discord da equipe e análise de logs do WhatsApp)
- **Participantes:** Victor Gabriel da Silva Menezes, Luiz Henrique Santos da Graça, Marcus Vinícius da Silva Araújo.
- **Descrição e Resultados:**
  A equipe analisou o histórico recente de mensagens nos grupos de WhatsApp utilizados pelos estudantes do CI e pelos restaurantes parceiros. O objetivo foi mapear as principais falhas do fluxo atual.
  **Resultados Obtidos:**
  - Identificou-se que a contagem de pedidos é feita manualmente pelo restaurante através da leitura de mensagens, gerando erros e perda de mensagens.
  - Constatou-se a dificuldade do restaurante em avisar rapidamente quando um prato acaba, resultando em estudantes pagando por refeições indisponíveis.
  - Levantou-se a necessidade de um sistema rigoroso de datas, impedindo pedidos para dias que não possuam cardápio publicado.

## Técnica 2: Entrevista Semi-Estruturada e Brainstorming

- **Data:** 10/10/2026
- **Local:** Centro de Informática (CI) - UFPB (Reunião remota)
- **Participantes:** Antônio Francelino de Pontes Neto, Kevin Gabriel Morais Mangueira e um representante do restaurante que oferta para alunos do CI.
- **Descrição e Resultados:**
  Foi conduzida uma entrevista semi-estruturada para entender o fluxo de trabalho sob a ótica do restaurante, seguida de um brainstorming para definir funcionalidades de mitigação de problemas.
  **Resultados Obtidos:**
  - O represetante do Restaurante relatou a necessidade de poder publicar cardápios "em lote" (semanais) para otimizar o tempo, em vez de publicar um por dia.
  - Definiu-se o conceito de "Indisponibilidade": um botão de emergência que o gestor aciona quando um insumo acaba, que deve refletir no sistema cancelando automaticamente os agendamentos pendentes daquele prato e acionando o estorno pelo gateway de pagamento.
  - Delimitou-se o escopo negativo: o sistema não fará gestão do estoque de insumos (arroz, feijão cru, etc.), apenas do "prato final" oferecido.