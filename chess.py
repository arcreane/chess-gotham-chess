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
    #创建玩家，包含名字颜色
    ai_player = AIPlayer(human_color)
    #创建AI并反选颜色
    self.players = [human_player, ai_player]
    #保存玩家
    if human_color == 0:
      self.currentPlayer = human_player
    else:
      self.currentPlayer = ai_player
      #执白先走

  def displayBoard(self):
      print(self.board)

  def isValidMove(self, move):
      pass

  def isCheckMate(self):
      pass

  def updateBoard(self, move):
      pass

  def switchPlayer(self):
      pass

  def play(self):
      pass
   
  
