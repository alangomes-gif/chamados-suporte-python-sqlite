"""Verifica persistência entre execuções reais do comando."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('chamados.py').resolve()

class TestPersistenciaCLI(unittest.TestCase):
    def test_fluxo_persiste_e_rejeita_salto(self):
        with tempfile.TemporaryDirectory(prefix='chamados teste ') as pasta:
            banco = Path(pasta) / 'exemplo.db'
            def executar(*args):
                return subprocess.run([sys.executable, str(SCRIPT), '--banco', str(banco), *args], capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING':'utf-8'}, timeout=15)
            novo = executar('abrir', 'Impressora fictícia sem conexão', '--prioridade', 'alta')
            self.assertEqual(novo.returncode, 0, novo.stderr)
            self.assertIn('Chamado criado: 1', novo.stdout)
            salto = executar('mover', '1', 'resolvido')
            self.assertEqual(salto.returncode, 2)
            estado = executar('listar')
            self.assertIn('aberto', estado.stdout)
            for destino in ['em_atendimento', 'resolvido']:
                resultado = executar('mover', '1', destino)
                self.assertEqual(resultado.returncode, 0, resultado.stderr)
            consulta = executar('listar')
            self.assertEqual(consulta.returncode, 0, consulta.stderr)
            self.assertIn('1 | Impressora fictícia sem conexão | alta | resolvido', consulta.stdout)
            self.assertTrue(banco.is_file())

if __name__ == '__main__':
    unittest.main()
