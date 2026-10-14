# Documento de Visão

## 1. Motivação
A alimentação dos estudantes do Centro de Informática (CI) da Universidade Federal da Paraíba (UFPB) depende de restaurantes locais. Atualmente, a comunicação sobre cardápios e pedidos ocorre de forma informal, principalmente por WhatsApp. O projeto propõe centralizar esse processo para melhorar a organização dos pedidos e a previsibilidade para estudantes e restaurantes.

## 2. Problema
O processo informal pode causar:
- dificuldade para contar e consolidar pedidos;
- dificuldade para identificar quem solicitou cada prato e acompanhar pagamentos;
- pouca visibilidade das quantidades disponíveis;
- demora ou ruído na comunicação quando um prato fica indisponível;
- dificuldade para informar estudantes afetados e tratar pagamentos já realizados.

## 3. Visão do produto
O Sistema de Agendamento de Almoços será uma aplicação web para centralizar a divulgação de cardápios e o agendamento de almoços pelos estudantes, além de apoiar os restaurantes na organização das ofertas e dos pedidos. 

## 4. Escopo previsto
- cadastro e gerenciamento de usuários;
- consulta de cardápios publicados;
- publicação e manutenção de cardápios e pratos;
- agendamento de almoço para datas e itens disponíveis;
- acompanhamento e cancelamento de pedidos;
- gestão dos pedidos pelo restaurante;
- tratamento de indisponibilidade de pratos;
- pagamento online via PIX ou cartão (integração com gateway);
- estorno automático em caso de cancelamento pelo restaurante;
- notificações aos estudantes sobre o status do pedido.

## 5. Escopo negativo
A proposta inicial não inclui:
- gerenciamento de entrega/delivery (a premissa é a retirada do almoço pelo estudante);
- controle completo de estoque de ingredientes crus;
- gestão integral do fluxo de caixa financeiro do restaurante;
- agendamento de refeições que não sejam almoço (ex: jantar, lanches);
- chat de comunicação em tempo real entre estudantes e restaurantes.

## 6. Perfis de usuários
- **Estudante:** consulta cardápios, agenda almoço, realiza pagamento, acompanha pedidos e solicita cancelamentos.
- **Gestor de Restaurante:** mantém informações do restaurante, pratos e cardápios, marca indisponibilidades e acompanha os pedidos.
- **Administrador:** administra usuários do sistema e gerencia os restaurantes cadastrados.
- **Gateway de Pagamento (Sistema Externo):** processa pagamentos online e solicitações automáticas de estorno.

## 7. Restrições e premissas iniciais
- O sistema será uma aplicação web acessível por navegadores em computadores e dispositivos móveis.
- Um agendamento depende obrigatoriamente de um cardápio válido e publicado para a data selecionada.
- O sistema limitará inicialmente o atendimento aos dois restaurantes principais que servem o CI da UFPB.