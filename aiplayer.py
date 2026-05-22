import random
from player import Player
class AIPlayer(Player):
  """Classe qui represente un joueur controle par l'ordinateur"""
  def __init__(self, color):
    """Initialise un joueur IA
    color :0 pour blanc, 1 pour noir"""
    super().__init__("AIPlayer", color)
  def askMove(self):
    """Genere un mouvement aleatoire"""
    pieces = ["K", "Q", "B", "N", "R", "P"]
    columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
    rows = [1, 2, 3, 4, 5, 6, 7, 8]
    piece = random.choice(pieces)
    start_column = random.choice(columns)
    start_row = random.choice(rows)
    end_column = random.choice(columns)
    end_row = random.choice(rows)
    move = piece + start_column + str(start_row) + " " + end_column + str(end_move)
    return move
