import sqlite3
import unittest
from chamados import conectar, abrir, transicionar, listar, historico

class TestHistorico(unittest.TestCase):
    def setUp(self):
        self.conn=conectar(':memory:')
        self.addCleanup(self.conn.close)
        self.ident=abrir(self.conn, 'Chamado fictício')

    def test_registra_transicoes_na_ordem(self):
        transicionar(self.conn,self.ident,'em_atendimento')
        transicionar(self.conn,self.ident,'resolvido')
        eventos=historico(self.conn,self.ident)
        self.assertEqual([(x[0],x[1]) for x in eventos],[('aberto','em_atendimento'),('em_atendimento','resolvido')])
        self.assertTrue(all(x[2].endswith('+00:00') for x in eventos))

    def test_transicao_rejeitada_nao_gera_evento(self):
        with self.assertRaises(ValueError):
            transicionar(self.conn,self.ident,'resolvido')
        self.assertEqual(historico(self.conn,self.ident),[])

    def test_falha_de_gravacao_desfaz_mudanca(self):
        self.conn.execute("CREATE TRIGGER falhar_historico BEFORE INSERT ON historico BEGIN SELECT RAISE(ABORT,'falha simulada'); END")
        with self.assertRaises(sqlite3.IntegrityError):
            transicionar(self.conn,self.ident,'em_atendimento')
        self.assertEqual(listar(self.conn)[0][3],'aberto')
        self.assertEqual(historico(self.conn,self.ident),[])

if __name__=='__main__':
    unittest.main()
