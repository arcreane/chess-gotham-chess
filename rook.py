from piece import Piece
from position import Position

class Rook(Piece):
    """Classe qui represente une tour aux echecs"""
    def __init__(self, position, color):
        """Initialise une tour.
        position: objet Position
        color: 0 pour blanc, 1 pour noir"""
        super().__init__(position, color)
    def __str__(self) -> str:
        """Renvoie la lettre utilisee pour representer la tour."""
        return "R"
    def isValidMove(self, newPosition, board) -> bool:
        """Verifie si le deplacement de la tour est valide.
        La tour peut se deplacer horizontalement ou verticalement.
        Elle ne peut pas sauter par-dessus une autre piece.
        Elle ne peut pas aller sur une piece de la meme couleur."""
        currentPosition = self.position
        #La tour ne peut pas rester sur la meme case
        if currentPosition == newPosition:
            return False
        #Verification simple que la destination est dans l'echiquier
        if newPosition.row < 1 or newPosition.row > 8:
            return False
        if newPosition.column < "a" or newPosition.column > "h":
            return False
        same_column = currentPosition.column == newPosition.column
        same_row = currentPosition.row == newPosition.row
        #La tour doit rester sur la meme ligne ou la meme colonne
        if not same_column and not same_row:
            return False
        #La tour ne peut pas capturer une piece de la meme couleur
        piece_destination = board.getPiece(newPosition)
        if piece_destination is not None and piece_destination.color == self.color:
            return False
        #cas 1: deplacement vertical
        if same_column:
            if newPosition.row > currentPosition.row:
                step = 1
            else:
                step = -1
            row = currentPosition.row + step
            while row != newPosition.row:
                position_to_check = Position(currentPosition.column, row)
                if board.getPiece(position_to_check) is not None:
                    return False
                row = row + step
        #cas 2: deplacement horizontal
        if same_row:
            current_col = currentPosition.get_column_idx()
            new_col = newPosition.get_column_idx()
            if new_col > current_col:
                step = 1
            else:
                step = -1
            col = current_col + step
            while col != new_col:
                column = chr(ord("a") + col)
                position_to_check = Position(column, currentPosition.row)
                if board.getPiece(position_to_check) is not None:
                    return False
                col = col + step
        return True
