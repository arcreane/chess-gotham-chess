from piece import Piece

class Pawn(Piece):
    
    def __str__(self) -> str:
        #Renvoie 'P' pour un pion blanc, 'p' pour un pion noir.
        return "P" if self.color == 0 else "p"

    def isValidMove(self, newPosition, board) -> bool:
        col_depart = self.position.get_column_idx()
        col_arrivee = newPosition.get_column_idx()
        
        row_depart = self.position.row
        row_arrivee = newPosition.row

        # Déplacement
        # Un pion blanc (0) monte (les lignes augmentent : +1 ou +2)
        # Un pion noir (1) descend (les lignes diminuent : -1 ou -2)
        direction = 1 if self.color == 0 else -1

        # calcul des écarts
        diff_col = col_arrivee - col_depart
        diff_row = row_arrivee - row_depart

        # logique des mvts
        
        # Cas A : Le pion avance tout droit de 1 case
        if diff_col == 0 and diff_row == direction:
            return True

        # Cas B : Le pion avance tout droit de 2 cases (uniquement au premier coup)
        ligne_depart_initiale = 2 if self.color == 0 else 7
        if diff_col == 0 and row_depart == ligne_depart_initiale and diff_row == 2 * direction:
            return True

        # Cas C : Le pion mange en diagonale (1 case en avant, 1 case sur le côté)
        # Note : Pour l'instant on valide juste la géométrie du mouvement à blanc.
        if abs(diff_col) == 1 and diff_row == direction:
            return True

        return False


#Test
if __name__ == "__main__":
    from position import Position
    
    print(" Test Bloc start")
    
    # Test 1 : Pion Blanc en position initiale (e2)
    pion_blanc = Pawn(Position("e", 2), 0)
    
    # Avancer de 1 case (e2 -> e3) : Attendu True
    print(f"Test 1 (e2 -> e3) : {pion_blanc.isValidMove(Position('e', 3), None)}")
    
    # Avancer de 2 cases au premier coup (e2 -> e4) : Attendu True
    print(f"Test 2 (e2 -> e4) : {pion_blanc.isValidMove(Position('e', 4), None)}")
    
    # Reculer (e2 -> e1) : Attendu False (un pion ne recule jamais)
    print(f"Test 3 (e2 -> e1) : {pion_blanc.isValidMove(Position('e', 1), None)}")
    
    # Test 2 : Pion Noir en position initiale (e7)
    pion_noir = Pawn(Position("e", 7), 1)
    
    # Avancer de 2 cases pour le noir (e7 -> e5) : Attendu True (car il descend)
    print(f"Test 4 (e7 -> e5) : {pion_noir.isValidMove(Position('e', 5), None)}")