from player import Player, chooseColor
from aiplayer import AIPlayer
class Chess:
  def __init__(self, board=None, players=None):
      self.board = board
      self.players = players if players is not None else []
      self.currentPlayer =None
  
  def initPlayers(self):
    """Initialise les deux joueurs de la partie"""
    name = input("Entrez votre nom : ")
    human_color = chooseColor()
    human_player = Player(name, human_color)
    ai_player = AIPlayer(human_color)
    self.players = [human_player, ai_player]
    if human_color == 0:
      self.currentPlayer = human_player
    else:
      self.currentPlayer = ai_player

  def displayBoard(self):
      print(self.board)

  def isValidMove(self, move):
      return True

  def isCheckMate(self):
      return False

  def updateBoard(self, move):
      pass

  def switchPlayer(self):
      pass

  def play(self):
      pass
   
  
