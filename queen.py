from piece import Piece

class Queen(Piece):
    """
    Classe représentant la Reine, elle hérite de la classe Piece.
    """

    def __str__(self) -> str:
        """Renvoie l'identifiant de la Reine selon le CDC"""
        return "Q"

    def isValidMove(self, newPosition, board) -> bool:
        # On utilise la méthode de notre classe Position
        col_depart = self.position.get_column_idx()
        col_arrivee = newPosition.get_column_idx()
        
        row_depart = self.position.row
        row_arrivee = newPosition.row

        diff_col = abs(col_depart - col_arrivee)
        diff_row = abs(row_depart - row_arrivee)

        # (Le reste de la logique de la Reine reste identique avec is_horizontal, etc.)
        if (diff_row == 0) or (diff_col == 0) or (diff_col == diff_row):
            return True
        return False
