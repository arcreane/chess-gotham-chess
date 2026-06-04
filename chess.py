from player import Player, chooseColor
from aiplayer import AIPlayer
from position import Position

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
    ai_player = AIPlayer(1-human_color)
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

  def parseMove(self, move):
      parts = move.split()
      if len(parts) != 2:
         return None

      start = parts[0]
      end = parts[1]

      if len(start) != 3 or len(end) != 3:
         return None
      
      piece_letter = start[0]

      start_position = Position(start[1], int(start[2]))
      end_position = Position(end[1], int(end[2]))

      return piece_letter, start_position, end_position
  
  def isValidMove(self, move):
      parsed_move = self.parseMove(move)

      if parsed_move is None:
        return False

      piece_letter, start_position, end_position = parsed_move
      piece = self.board.getPiece(start_position)

      if piece is None:
        return False

      if str(piece) != piece_letter:
        return False

      if piece.color != self.currentPlayer.color:
        return False

      return piece.isValidMove(end_position, self.board)
    
  
        
  def isCheckMate(self):
      return False

  
  def updateBoard(self, move):
     parsed_move = self.parseMove(move)

     if parsed_move is None:
        return
     piece_letter, start_position, end_position = parsed_move
     piece = self.board.getPiece(start_position)
    
     if piece is not None:
        piece.position = end_position
  

  def switchPlayer(self):
     if self.currentPlayer == self.players[0]:
        self.currentPlayer = self.players[1]
     else:
        self.currentPlayer = self.players[0]
       
        

  def play(self):
      self.initPlayers()

      while not self.isCheckMate():
            self.displayBoard()

            move = self.currentPlayer.askMove()

            while not self.isValidMove(move):
                  print("Mouvement invalide.")
                  move = self.currentPlayer.askMove()

            self.updateBoard(move)
            self.switchPlayer()
   
  
