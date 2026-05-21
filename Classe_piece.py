from abc import ABC, abstractmethod

class Piece(ABC):
    """
    Toutes les pièces doivent hériter de cette classe
    """
    def __init__(self, position, color):
        self.position = position  # Objet de type Position
        self.color = color        # 0 pour Blanc, 1 pour Noir

    @abstractmethod
    def isValidMove(self, newPosition, board) -> bool:
        """
        Cette méthode doit être remplie par chaque pièce. 
        Elle vérifie si le déplcement vers newPosition est légal.
        Elle doit renvoyer True si le mouvement est autorisé, sinon False.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Renvoie la lettre de la pièce (Q, R, B...)"""
        pass

#test
if __name__ == "__main__":
    try:
        p = Piece(None, 0)
        print("Erreur : J'ai créé une pièce abstraite.")
    except TypeError as e:
        print("Test réussi, Impossible de créer une pièce générique.")
        print(f"Message de Python : {e}")
