import unittest
import os
import sys

# Añadir la raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game_logic import GameLogic

class TestGameLogic(unittest.TestCase):
    def test_add_points(self):
        game = GameLogic()
        self.assertEqual(game.add_points(10), 10)
        self.assertEqual(game.add_points(-5), 10)  # No debe sumar puntos negativos

if __name__ == "__main__":
    unittest.main()
