from piece import Piece
from position import Position

class Knight(Piece):
  def __str__(self):
    return "N"
  
  def isValidMove(self, newPosition, board):
      dx = abs(self.position.get_column_idx() - newPosition.get_column_idx())
      dy = abs(self.position.row - newPosition.row)

      if not ((dx == 1 and dy == 2) or ((dx == 2 and dy == 1)):
         return False

      piece_arrivee = board.getPiece(newPosition)

      if piece_arrivee is not None and piece_arrivee.color == self.color:
         return False
      return True

          
