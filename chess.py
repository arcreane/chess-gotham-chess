class Chess:
  def __init__(self, board=None, players=None):
      self.board = board
      self.players = players if players is not None else []
      self.currentPlayer =None
  
  def initPlayers(self):
      pass

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
   
  
