from piece import Piece
class Bishop(Piece):

    def __str__(self) -> str:
        return "B"
def isValidMove(self, newPosition, board) -> bool:
        col_depart = self.position.get_column_idx()
        col_arrivee = newPosition.get_column_idx()
        
        row_depart = self.position.row
        row_arrivee = newPosition.row

        diff_col = abs(col_depart - col_arrivee)
        diff_row = abs(row_depart - row_arrivee)

        if diff_row == diff_col and diff_row != 0:
            return True
            
        return False

if __name__ == "__main__":
    from position import Position
pos_depart = Position("d", 4)
    mon_fou = Bishop(pos_depart, 0)

    pos_valide = Position("f", 6)
    print(f"Test d4-f6 : {mon_fou.isValidMove(pos_valide, None)}")

    pos_invalide = Position("d", 6)
    print(f"Test d4-d6 : {mon_fou.isValidMove(pos_invalide, None)}")
