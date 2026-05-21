class Position:
    def __init__(self, column: str, row: int):
        # On force la colonne en minuscule (ex: 'A' devient 'a')
        self.column = column.lower()
        self.row = row

    def __str__(self) -> str:
        # Affiche la position proprement (ex: "d4")
        return f"{self.column}{self.row}"

    def get_column_idx(self) -> int:
        # Utile pour les calculs : transforme 'a' en 0, 'b' en 1, etc.
        return ord(self.column) - ord('a')

    def __eq__(self,other) -> bool:
        """Permet de savoir si deux pièces partagent la même case)"""
        if not isinstance(other, Position):
            return False
        return self.column == other.column and self.row == other.row
