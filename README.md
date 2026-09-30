# Sistema de Acompanhamento de Almoço CI

Sistema web para centralizar a divulgação de cardápios e o **agendamento de almoços** dos estudantes do **Centro de Informática (CI) da Universidade Federal da Paraíba (UFPB)**.

Projeto desenvolvido na disciplina **Métodos de Projeto de Software**.

---

## Integrantes

- Antônio Francelino de Pontes Neto
- Kevin Gabriel Morais Mangueira
- Luiz Henrique Santos da Graça
- Marcus Vinícius da Silva Araújo
- Victor Gabriel da Silva Menezes

## Contexto

Hoje o processo é informal e acontece pelo WhatsApp: os restaurantes divulgam o cardápio do dia em grupos ou conversas, e os estudantes enviam seus pedidos diretamente pelo aplicativo. Isso dificulta:

- a organização e a contagem dos pedidos;
- a identificação de quem pediu o quê;
- o controle das quantidades disponíveis;
- a comunicação quando algum prato acaba ou deixa de ser servido no dia.

## Solução proposta

Uma aplicação web em que:

- **restaurantes** publicam seus cardápios (por dia ou por semana), informam quais pratos estão disponíveis em cada dia e recebem os pedidos de forma organizada;
- **estudantes** consultam os cardápios publicados, agendam o almoço para uma data disponível, pagam e acompanham o status do pedido;
- **administradores** mantêm os usuários e os restaurantes cadastrados.
- **gateway de pagamento** processa os pagamentos via PIX ou cartão, consulta o status e estorna os pagamentos.

Inicialmente o sistema atenderá **dois restaurantes** que servem o CI, com arquitetura preparada para incluir novos estabelecimentos.

## Como funciona o agendamento

O agendamento é **amarrado ao cardápio publicado**:

1. O restaurante publica um cardápio **diário** (uma data) ou **semanal** (um intervalo de datas), definindo os pratos de cada dia.
2. O estudante só consegue agendar para as **datas cobertas por esse cardápio**. Não é possível agendar para datas passadas, para datas sem cardápio publicado ou para o próprio dia depois do horário limite do restaurante.
3. Se, no dia, algum prato (ou o almoço inteiro) **não puder ser servido**, o restaurante marca a indisponibilidade. Os pedidos afetados são cancelados automaticamente, os estudantes são notificados e os pagamentos já feitos são estornados.

## Perfis de usuário

| Perfil | O que faz |
|--------|-----------|
| **Estudante** | Cadastra-se com a matrícula, consulta cardápios, agenda, paga, acompanha e cancela pedidos. |
| **Gestor de Restaurante** | Gerencia os pratos, publica cardápios, informa indisponibilidades e atualiza o status dos pedidos. |
| **Administrador** | Cadastra e lista usuários, ativa/desativa contas e gerencia restaurantes. |
| **Gateway de Pagamento** | Processa pagamentos via PIX ou cartão, consulta status e estorna pagamentos. |