class Piece:
    """Classe de base pour une piece d'echecs."""

    def __init__(self, position, color):
        self.position = position
        self.color = color

class Position:
    """Classe qui represente une position."""

    def __init__(self, column, row):
        self.column = column
        self.row = row

    def __str__(self):
        return str(self.column) + str(self.row)

class Tour(Piece):
    """Classe qui represente une tour."""

    def __init__(self, position, color):
        super().__init__(position, color)

    def __str__(self):
        return "R"

    def isValidMove(self, newPosition, board):
        """
        Verifie si le deplacement de la tour est valide.

        newPosition : position d'arrivee
        board : plateau de jeu
        """
        currentPosition = self.position
#La tour ne peut pas rester sur la meme case
        if currentPosition.column == newPosition.column and currentPosition.row == newPosition.row:
            return False
#La tour se deplace seulement en ligne droute et soit sur la meme colonne soit sur la meme ligne
        same_column = currentPosition.column == newPosition.column
        same_row = currentPosition.row == newPosition.row

        if not same_column and not same_row:
            return False
#La tour ne peut pas aller sur une piece de la meme couleur
        piece_destination = board.getPiece(newPosition)

        if piece_destination is not None:
            if piece_destination.color == self.color:
                return False
#Verification du chemin si la tour monte ou descend
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
#Vetification du chemin si la tour va a gouche ou a droite
        if same_row:
            current_col_number = ord(currentPosition.column)
            new_col_number = ord(newPosition.column)

            if new_col_number > current_col_number:
                step = 1
            else:
                step = -1

            col_number = current_col_number + step

            while col_number != new_col_number:
                column = chr(col_number)
                position_to_check = Position(column, currentPosition.row)

                if board.getPiece(position_to_check) is not None:
                    return False

                col_number = col_number + step

        return True