# Chamados de suporte com Python e SQLite

Demonstração local de portfólio, com dados fictícios. Cria chamados e controla o fluxo aberto -> em_atendimento -> resolvido, rejeitando saltos de etapa.

Python 3.10+, sem dependências externas. Na pasta do projeto:

    python chamados.py --banco exemplo.db abrir "Impressora de demonstração sem conexão" --prioridade alta
    python chamados.py --banco exemplo.db mover 1 em_atendimento
    python chamados.py --banco exemplo.db mover 1 resolvido
    python chamados.py --banco exemplo.db listar
    python -m unittest -v

Consultas SQL parametrizadas; validação de título e prioridade; data em UTC. Seis testes verificam fluxo, rejeição sem alteração do estado, validação, ID inexistente e texto semelhante a SQL.

Limites: sem usuários, autenticação, anexos, SLA ou interface web. Não inserir informações reais de clientes. O teste de integração executa o comando em processos separados com banco temporário, verifica persistência, rejeição de salto de etapa e resolução do chamado.

## Histórico de transições

    python chamados.py --banco exemplo.db historico 1

Cada mudança válida registra estado anterior, novo estado e horário UTC na mesma transação SQLite. Se o registro do histórico falhar, a mudança de estado é desfeita. Transições rejeitadas não geram eventos. A suíte agora tem nove testes, incluindo uma falha de gravação simulada e consulta pelo terminal. O histórico só cobre transições realizadas a partir desta versão; não é um registro imutável e não inclui identidade de usuário.
