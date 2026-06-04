from piece import Piece
from position import Position

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

#bloc test
if __name__ == "__main__":
    print("Début du test")

    pos_depart = Position("d", 4)
    ma_reine = Queen(pos_depart, 0)

    pos_valide = Position("f", 6)
    print(f"Test 1 mouvement valide d4 à d6 (Attendu True) : {ma_reine.isValidMove(pos_valide, None)}")

    pos_invalide = Position("e", 6)
    print(f"Test 2 mouvement invalide d4 à e6 (Attendu False) : {ma_reine.isValidMove(pos_invalide, None)}")
