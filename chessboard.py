from position import Position

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
    
    def place_piece(self, piece, position):
        row = position.row -1
        col = position.get_column_idx()
        self.grid[row][col] = piece
        piece.position = position

    def get_piece_at(self, position):
        row = position.row -1
        col = position.get_column_idx()
        return self.grid[row][col]

    def move_piece(self, start_pos, end_pos):
        piece = self.get_piece_at(start_pos)
        if piece and piece.isValidMove(end_pos, self):
            self.grid[end_pos.row][end_pos.get_column_idx()] = piece
            self.grid[start_pos.row][start_pos.get_column_idx()] = None
            piece.position = end_pos
            return True
        return False
def __str__(self):
        display = "  a b c d e f g h\n"
        for r in range(7, -1, -1):
            line = f"{r} "
            for c in range(8):
                piece = self.grid[r][c]
                line += f"{piece if piece else '.'} "
            display += line + "\n"
        return display

if __name__ == "__main__":
    from queen import Queen
    from bishop import Bishop

    my_board = Board()
    
    pos_q = Position("d", 4)
    reine = Queen(pos_q, 0)
    my_board.place_piece(reine, pos_q)

    pos_b = Position("c", 1)
    fou = Bishop(pos_b, 1)
    my_board.place_piece(fou, pos_b)

    print("État de l'échiquier :")
    print(my_board)
