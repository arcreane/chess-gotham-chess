from piece import Piece
from position import Position

class King(Piece):

    def __str__(self) -> str:
        return "K" if self.color == 0 else "k"

    def isValidMove(self, newPosition, board) -> bool:
        col_depart = self.position.get_column_idx()
        col_arrivee = newPosition.get_column_idx()
        
        row_depart = self.position.row
        row_arrivee = newPosition.row

        diff_col = abs(col_depart - col_arrivee)
        diff_row = abs(row_depart - row_arrivee)

        if diff_row <= 1 and diff_col <= 1:
            if diff_row == 0 and diff_col == 0:
                return False
            return True
            
        return False


#Test
if __name__ == "__main__":
    print("test start")

    mon_roi = King(Position("e", 4), 0)
    
    # Test 1 : Déplacement d'une case tout droit (e4 -> e5) : True
    print(f"Test 1 (e4 -> e5) : {mon_roi.isValidMove(Position('e', 5), None)}")
    
    # Test 2 : Déplacement d'une case en diagonale (e4 -> f5) : True
    print(f"Test 2 (e4 -> f5) : {mon_roi.isValidMove(Position('f', 5), None)}")
    
    # Test 3 : Déplacement trop long de deux cases (e4 -> e6) : False
    print(f"Test 3 (e4 -> e6) : {mon_roi.isValidMove(Position('e', 6), None)}")
    
    # Test 4 : Rester sur place (e4 -> e4) : False
    print(f"Test 4 (e4 -> e4) : {mon_roi.isValidMove(Position('e', 4), None)}")