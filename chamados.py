"""Controle local de chamados de suporte com SQLite."""
import argparse
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

ESTADOS = {'aberto': {'em_atendimento'}, 'em_atendimento': {'resolvido'}, 'resolvido': set()}


def conectar(banco):
    conn = sqlite3.connect(banco)
    conn.execute('CREATE TABLE IF NOT EXISTS chamados (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, prioridade TEXT NOT NULL CHECK(prioridade IN (\'baixa\',\'media\',\'alta\')), estado TEXT NOT NULL DEFAULT \'aberto\' CHECK(estado IN (\'aberto\',\'em_atendimento\',\'resolvido\')), criado_em TEXT NOT NULL)')
    conn.commit()
    return conn


def abrir(conn, titulo, prioridade='media'):
    titulo = titulo.strip()
    if not titulo or len(titulo) > 200:
        raise ValueError('Título deve ter entre 1 e 200 caracteres')
    if prioridade not in {'baixa', 'media', 'alta'}:
        raise ValueError('Prioridade inválida')
    with conn:
        cursor = conn.execute('INSERT INTO chamados(titulo,prioridade,criado_em) VALUES(?,?,?)', (titulo, prioridade, datetime.now(timezone.utc).isoformat()))
    return cursor.lastrowid


def transicionar(conn, identificador, destino):
    with conn:
        linha = conn.execute('SELECT estado FROM chamados WHERE id=?', (identificador,)).fetchone()
        if linha is None:
            raise ValueError('Chamado inexistente')
        atual = linha[0]
        if destino not in ESTADOS[atual]:
            raise ValueError('Transição de estado não permitida')
        resultado = conn.execute('UPDATE chamados SET estado=? WHERE id=? AND estado=?', (destino, identificador, atual))
        if resultado.rowcount != 1:
            raise ValueError('Chamado alterado por outra operação')


def listar(conn):
    return conn.execute('SELECT id,titulo,prioridade,estado FROM chamados ORDER BY id').fetchall()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--banco', default='chamados.db')
    sub = parser.add_subparsers(dest='comando', required=True)
    novo = sub.add_parser('abrir')
    novo.add_argument('titulo')
    novo.add_argument('--prioridade', choices=['baixa', 'media', 'alta'], default='media')
    mudar = sub.add_parser('mover')
    mudar.add_argument('id', type=int)
    mudar.add_argument('estado', choices=list(ESTADOS))
    sub.add_parser('listar')
    args = parser.parse_args()
    with closing(conectar(args.banco)) as conn:
        try:
            if args.comando == 'abrir':
                print('Chamado criado:', abrir(conn, args.titulo, args.prioridade))
            elif args.comando == 'mover':
                transicionar(conn, args.id, args.estado)
                print('Estado atualizado')
            else:
                for linha in listar(conn):
                    print(' | '.join(map(str, linha)))
        except ValueError as erro:
            parser.error(str(erro))


if __name__ == '__main__':
    main()
