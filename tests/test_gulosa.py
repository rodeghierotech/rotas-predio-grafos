import unittest

from buscas import gulosa


class TestGulosa(unittest.TestCase):
    def test_gulosa_escolhe_o_vizinho_mais_perto_sem_retroceder(self):
        """Protege a regra do enunciado de seguir sem voltar atras."""
        grafo = {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1)],
            "C": [("A", 2), ("D", 1)],
            "D": [("C", 1)],
        }

        caminho, custo, visitados = gulosa(grafo, "A", "D")

        self.assertEqual(caminho, [])
        self.assertEqual(custo, 0)
        self.assertEqual(visitados, 2)
