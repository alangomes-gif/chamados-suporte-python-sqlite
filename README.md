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
