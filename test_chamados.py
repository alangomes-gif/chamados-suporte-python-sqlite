import unittest
from chamados import conectar, abrir, listar, transicionar

class TestChamados(unittest.TestCase):
    def setUp(self):
        self.conn = conectar(':memory:')
        self.addCleanup(self.conn.close)

    def test_fluxo_completo(self):
        ident = abrir(self.conn, 'Impressora de demonstração sem conexão', 'alta')
        transicionar(self.conn, ident, 'em_atendimento')
        transicionar(self.conn, ident, 'resolvido')
        self.assertEqual(listar(self.conn)[0][3], 'resolvido')

    def test_pular_etapa_nao_altera_estado(self):
        ident = abrir(self.conn, 'Teste')
        with self.assertRaises(ValueError):
            transicionar(self.conn, ident, 'resolvido')
        self.assertEqual(listar(self.conn)[0][3], 'aberto')

    def test_invalidos_nao_sao_gravados(self):
        for titulo, prioridade in [('', 'media'), ('x'*201, 'alta'), ('Teste', 'urgente')]:
            with self.assertRaises(ValueError):
                abrir(self.conn, titulo, prioridade)
        self.assertEqual(listar(self.conn), [])

    def test_texto_sql_e_tratado_como_dado(self):
        texto = "'); DROP TABLE chamados;--"
        abrir(self.conn, texto)
        abrir(self.conn, 'Outro')
        self.assertEqual(listar(self.conn)[0][1], texto)
        self.assertEqual(len(listar(self.conn)), 2)

    def test_inexistente(self):
        with self.assertRaises(ValueError):
            transicionar(self.conn, 999, 'em_atendimento')

if __name__ == '__main__':
    unittest.main()
