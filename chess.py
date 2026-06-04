import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import random
import pickle
from abc import ABC, abstractmethod

class Position:
    def __init__(self, column: str, row: int):
        self.column = column.lower()
        self.row = row

    def __str__(self):
        return f"{self.column}{self.row}"

    def copy(self):
        return Position(self.column, self.row)

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.column == other.column and self.row == other.row
        return False

class Piece(ABC):
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.has_moved = False

    @abstractmethod
    def is_valid_move(self, new_pos, board):
        pass

class King(Piece):
    def __str__(self): return "K"

    def is_valid_move(self, new_pos, board):
        dc = abs(ord(new_pos.column) - ord(self.position.column))
        dr = abs(new_pos.row - self.position.row)

        if max(dc, dr) == 1: return True

        if not self.has_moved and dr == 0:
            if dc == 2 and new_pos.column == 'g':
                if board.chess.is_check(self.color): return False
                rook = board.get_piece(Position('h', self.position.row))
                if rook and not rook.has_moved:
                    if board.chess.would_cause_check(self, Position('f', self.position.row)): return False
                    return board.is_path_clear(self.position, Position('h', self.position.row))

            if dc == 2 and new_pos.column == 'c':
                if board.chess.is_check(self.color): return False
                rook = board.get_piece(Position('a', self.position.row))
                if rook and not rook.has_moved:
                    if board.chess.would_cause_check(self, Position('d', self.position.row)): return False
                    return board.is_path_clear(self.position, Position('a', self.position.row))
        return False

class Queen(Piece):
    def __str__(self): return "Q"
    def is_valid_move(self, new_pos, board):
        dc = abs(ord(new_pos.column) - ord(self.position.column))
        dr = abs(new_pos.row - self.position.row)
        if dc == dr or dc == 0 or dr == 0:
            return board.is_path_clear(self.position, new_pos)
        return False

class Bishop(Piece):
    def __str__(self): return "B"
    def is_valid_move(self, new_pos, board):
        dc = abs(ord(new_pos.column) - ord(self.position.column))
        dr = abs(new_pos.row - self.position.row)
        return dc == dr and board.is_path_clear(self.position, new_pos)

class Knight(Piece):
    def __str__(self): return "N"
    def is_valid_move(self, new_pos, board):
        dc = abs(ord(new_pos.column) - ord(self.position.column))
        dr = abs(new_pos.row - self.position.row)
        return (dc, dr) in [(1, 2), (2, 1)]

class Rook(Piece):
    def __str__(self): return "R"
    def is_valid_move(self, new_pos, board):
        same_col = self.position.column == new_pos.column
        same_row = self.position.row == new_pos.row
        if same_col or same_row:
            return board.is_path_clear(self.position, new_pos)
        return False

class Pawn(Piece):
    def __str__(self): return "P"
    def is_valid_move(self, new_pos, board):
        direction = 1 if self.color == 0 else -1
        dc = ord(new_pos.column) - ord(self.position.column)
        dr = new_pos.row - self.position.row
        target = board.get_piece(new_pos)

        if dc == 0:
            if dr == direction and target is None: return True
            start_row = 2 if self.color == 0 else 7
            if self.position.row == start_row and dr == 2 * direction:
                middle = Position(self.position.column, self.position.row + direction)
                return board.get_piece(middle) is None and target is None

        if abs(dc) == 1 and dr == direction:
            if target and target.color != self.color: return True
        return False

class Board:
    def __init__(self):
        self.pieces = []
        self.board = {}
        self.chess = None 

    def add_piece(self, piece):
        self.pieces.append(piece)
        self.board[str(piece.position)] = piece

    def get_piece(self, position):
        return self.board.get(str(position))

    def init_board(self):
        self.pieces = []
        self.board = {}
        for i, p_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            col = chr(ord('a') + i)
            self.add_piece(p_class(Position(col, 1), 0))
            self.add_piece(Pawn(Position(col, 2), 0))
            self.add_piece(p_class(Position(col, 8), 1))
            self.add_piece(Pawn(Position(col, 7), 1))

    def is_path_clear(self, start, end):
        sc, ec = ord(start.column), ord(end.column)
        sr, er = start.row, end.row
        dc = 0 if ec == sc else (1 if ec > sc else -1)
        dr = 0 if er == sr else (1 if er > sr else -1)
        c, r = sc + dc, sr + dr
        while c != ec or r != er:
            if self.get_piece(Position(chr(c), r)): return False
            c += dc
            r += dr
        return True

    def move_piece(self, piece, new_pos):
        old = str(piece.position)
        if old in self.board: del self.board[old]

        target = self.get_piece(new_pos)
        if target:
            self.pieces.remove(target)

        if isinstance(piece, King):
            if old == 'e1' and str(new_pos) == 'g1':
                rook = self.get_piece(Position('h', 1))
                self.move_piece(rook, Position('f', 1))
            elif old == 'e1' and str(new_pos) == 'c1':
                rook = self.get_piece(Position('a', 1))
                self.move_piece(rook, Position('d', 1))
            elif old == 'e8' and str(new_pos) == 'g8':
                rook = self.get_piece(Position('h', 8))
                self.move_piece(rook, Position('f', 8))
            elif old == 'e8' and str(new_pos) == 'c8':
                rook = self.get_piece(Position('a', 8))
                self.move_piece(rook, Position('d', 8))

        piece.position = new_pos
        piece.has_moved = True
        self.board[str(new_pos)] = piece

class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def choose_move(self, chess, color):
        moves = []
        for piece in chess.board.pieces:
            if piece.color != color: continue
            for c in 'abcdefgh':
                for r in range(1, 9):
                    pos = Position(c, r)
                    if chess.is_valid_move(piece.position, pos):
                        moves.append((piece.position.copy(), pos))

        if not moves: return None

        captures = []
        for move in moves:
            target = chess.board.get_piece(move[1])
            if target: captures.append(move)

        if captures and self.difficulty == 'medium': return random.choice(captures)
        return random.choice(moves)

class Chess:
    def __init__(self):
        self.board = Board()
        self.board.chess = self
        self.board.init_board()
        self.current = 0
        self.last_move = None
        self.position_history = []
        self.save_position_state()
        
    def switch_player(self):
        self.current = 1 - self.current
        self.save_position_state()
    
    def save_position_state(self):
        state = []
        for pos_str, piece in sorted(self.board.board.items()):
            state.append(f"{pos_str}:{piece}{piece.color}")
        state.append(str(self.current))
        self.position_history.append("-".join(state))
        
    def has_legal_moves(self, color):
        for piece in self.board.pieces:
            if piece.color != color: continue
            for c in 'abcdefgh':
                for r in range(1, 9):
                    pos = Position(c, r)
                    if self.is_valid_move(piece.position, pos): return True
        return False

    def is_insufficient_material(self):
        pieces = self.board.pieces
        if len(pieces) == 2: return True
        if len(pieces) == 3:
            for p in pieces:
                if isinstance(p, (Bishop, Knight)): return True
        return False

    def is_threefold_repetition(self):
        if not self.position_history: return False
        current_state = self.position_history[-1]
        return self.position_history.count(current_state) >= 3

    def check_game_over(self):
        if self.is_insufficient_material(): return 'stalemate_material'
        if self.is_threefold_repetition(): return 'stalemate_repetition'
        
        if not self.has_legal_moves(self.current):
            if self.is_check(self.current): return 'checkmate'
            else: return 'stalemate_no_moves'
        return None
    
    def is_check(self, color):
        king = next((p for p in self.board.pieces if isinstance(p, King) and p.color == color), None)
        if king is None: return False
        for p in self.board.pieces:
            if p.color != color and p.is_valid_move(king.position, self.board): return True
        return False

    def would_cause_check(self, piece, end):
        old_pos = piece.position.copy()
        captured = self.board.get_piece(end)

        if captured: self.board.pieces.remove(captured)
        del self.board.board[str(old_pos)]
        piece.position = end
        self.board.board[str(end)] = piece

        check = self.is_check(piece.color)

        del self.board.board[str(end)]
        piece.position = old_pos
        self.board.board[str(old_pos)] = piece
        if captured:
            self.board.pieces.append(captured)
            self.board.board[str(end)] = captured

        return check

    def is_valid_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece is None or piece.color != self.current: return False
        target = self.board.get_piece(end)
        if target and target.color == piece.color: return False
        if not piece.is_valid_move(end, self.board): return False
        if self.would_cause_check(piece, end): return False
        return True

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("♔ Jeu d'Échecs ♚")
        self.root.geometry("850x620")
        self.root.configure(bg="#2c3e50")
        
        self.square_size = 55
        self.margin = 40
        
        self.show_menu()

    def show_menu(self):
        self.in_game = False 
        for w in self.root.winfo_children(): w.destroy()

        menu_frame = tk.Frame(self.root, bg="#2c3e50")
        menu_frame.pack(expand=True)

        tk.Label(menu_frame, text="♔ Jeu d'Échecs ♚", font=("Helvetica", 38, "bold"), bg="#2c3e50", fg="white").pack(pady=40)

        btn_style = {"font": ("Arial", 14, "bold"), "fg": "white", "width": 25, "height": 2, "bd": 0}
        tk.Button(menu_frame, text="👥 Joueur vs Joueur", command=self.start_pvp, bg="#27ae60", **btn_style).pack(pady=15)
        tk.Button(menu_frame, text="🤖 Jouer contre l'IA", command=lambda: self.start_ai('medium'), bg="#2980b9", **btn_style).pack(pady=15)

    def start_pvp(self):
        self.chess = Chess()
        self.ai = None
        self.init_game()

    def start_ai(self, difficulty):
        self.chess = Chess()
        self.ai = AI(difficulty)
        self.init_game()

    def init_game(self):
        for w in self.root.winfo_children(): w.destroy()

        self.main = tk.Frame(self.root, bg="#2c3e50")
        self.main.pack(fill="both", expand=True, padx=15, pady=15)

        self.left = tk.Frame(self.main, bg="#2c3e50")
        self.left.pack(side="left")
        self.right = tk.Frame(self.main, bg="#34495e", padx=15, pady=15, bd=2, relief="groove")
        self.right.pack(side="right", fill="y", expand=True)

        self.status_frame = tk.Frame(self.left, bg="#ecf0f1", bd=3, relief="ridge")
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        self.status = tk.Label(self.status_frame, text="", font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50", pady=8)
        self.status.pack()

        c_size = 8 * self.square_size + 2 * self.margin
        self.canvas = tk.Canvas(self.left, width=c_size, height=c_size, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        tk.Label(self.right, text="Historique", font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack(pady=5)
        self.history = scrolledtext.ScrolledText(self.right, width=24, height=16, bg="#2c3e50", fg="white", font=("Consolas", 11), borderwidth=0)
        self.history.pack(pady=10, fill="both", expand=True)
        self.history.config(state=tk.DISABLED)

        btn_style = {"font": ("Arial", 10, "bold"), "fg": "white", "width": 18, "height": 1, "bd": 0}
        tk.Button(self.right, text="💾 Sauvegarder", command=self.save_game, bg="#27ae60", **btn_style).pack(pady=5)
        tk.Button(self.right, text="📂 Charger", command=self.load_game, bg="#d35400", **btn_style).pack(pady=5)
        tk.Button(self.right, text="🚪 Menu", command=self.show_menu, bg="#c0392b", **btn_style).pack(pady=5)

        self.selected = None
        self.valid_moves_cache = []
        
        self.update_status()
        self.draw_board()

    def get_unicode(self, piece):
        symbols = {"P": ("♙", "♟"), "R": ("♖", "♜"), "N": ("♘", "♞"), "B": ("♗", "♝"), "Q": ("♕", "♛"), "K": ("♔", "♚")}
        return symbols[str(piece)][piece.color]

    def get_piece_name(self, piece):
        noms = {"P": "Pion", "R": "Tour", "N": "Cavalier", "B": "Fou", "Q": "Reine", "K": "Roi"}
        return noms[str(piece).upper()]

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#EEEED2", "#769656"]

        for i in range(8):
            y_center = self.margin + (7 - i) * self.square_size + self.square_size // 2
            self.canvas.create_text(self.margin // 2, y_center, text=str(i + 1), fill="white", font=("Arial", 12, "bold"))
            
            x_center = self.margin + i * self.square_size + self.square_size // 2
            self.canvas.create_text(x_center, self.margin + 8 * self.square_size + self.margin // 2, text=chr(ord('a') + i), fill="white", font=("Arial", 12, "bold"))

        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                
                x1 = self.margin + c * self.square_size
                y1 = self.margin + (7 - r) * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                if self.selected and self.selected.row - 1 == r and ord(self.selected.column) - ord('a') == c:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F6F669", outline="")

                piece = self.chess.board.get_piece(Position(chr(c + ord('a')), r + 1))
                if piece:
                    self.canvas.create_text(x1 + self.square_size//2, y1 + self.square_size//2, text=self.get_unicode(piece), font=("Arial", 36))

        if self.selected:
            for pos in self.valid_moves_cache:
                cx = self.margin + (ord(pos.column) - ord('a')) * self.square_size + self.square_size // 2
                cy = self.margin + (8 - pos.row) * self.square_size + self.square_size // 2
                self.canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="#00FF88", outline="")

        if self.chess.check_game_over(): self.draw_victory_screen()

    def on_click(self, event):
        if self.chess.check_game_over() or (self.ai and self.chess.current == 1): return
        
        if event.x < self.margin or event.x > self.margin + 8 * self.square_size: return
        if event.y < self.margin or event.y > self.margin + 8 * self.square_size: return

        col_idx = (event.x - self.margin) // self.square_size
        row_idx = 7 - ((event.y - self.margin) // self.square_size)
        clicked = Position(chr(col_idx + ord('a')), row_idx + 1)

        piece = self.chess.board.get_piece(clicked)

        if self.selected is None:
            if piece and piece.color == self.chess.current:
                self.selected = clicked
                self.cache_valid_moves(piece)
        else:
            if clicked in self.valid_moves_cache:
                moving_piece = self.chess.board.get_piece(self.selected)
                self.execute_move(moving_piece, self.selected, clicked)
            
            self.selected = None
            self.valid_moves_cache.clear()
        
        self.draw_board()

    def cache_valid_moves(self, piece):
        self.valid_moves_cache.clear()
        for r in range(1, 9):
            for c in 'abcdefgh':
                pos = Position(c, r)
                if self.chess.is_valid_move(piece.position, pos):
                    self.valid_moves_cache.append(pos)

    def execute_move(self, piece, start, end):
        self.chess.last_move = (start.copy(), end.copy())
        self.chess.board.move_piece(piece, end)

        nom_piece = self.get_piece_name(piece)
        joueur = "Blancs" if piece.color == 0 else "Noirs"
        
        self.history.config(state=tk.NORMAL)
        self.history.insert(tk.END, f"[{joueur}]\n {nom_piece} {start} -> {end}\n")
        self.history.see(tk.END)
        self.history.config(state=tk.DISABLED)

        if isinstance(piece, Pawn) and (end.row == 8 or end.row == 1):
            if self.ai and piece.color == 1: 
                new_piece = Queen(end, 1)
                self.chess.board.pieces.remove(piece)
                self.chess.board.add_piece(new_piece)
                self.log_promotion(new_piece)
            else: 
                self.draw_board() 
                self.promote(piece)
        else:
            self.history.config(state=tk.NORMAL)
            self.history.insert(tk.END, "\n")
            self.history.config(state=tk.DISABLED)

        self.chess.switch_player()
        self.update_status()
        self.draw_board()

        if self.ai and self.chess.check_game_over() is None and self.chess.current == 1:
            self.root.after(600, self.play_ai)

    def log_promotion(self, nouvelle_piece):
        self.history.config(state=tk.NORMAL)
        self.history.insert(tk.END, f" (Promu: {self.get_piece_name(nouvelle_piece)})\n\n")
        self.history.see(tk.END)
        self.history.config(state=tk.DISABLED)

    def play_ai(self):
        move = self.ai.choose_move(self.chess, 1)
        if move:
            piece = self.chess.board.get_piece(move[0])
            self.execute_move(piece, move[0], move[1])

    def promote(self, pawn):
        popup = tk.Toplevel(self.root)
        popup.title("Promotion")
        popup.geometry("380x150")
        popup.configure(bg="#2c3e50")
        
        tk.Label(popup, text="Choisissez une pièce :", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
        frame = tk.Frame(popup, bg="#2c3e50")
        frame.pack()
        
        def set_piece(cls):
            nouvelle_piece = cls(pawn.position, pawn.color)
            self.chess.board.pieces.remove(pawn)
            self.chess.board.add_piece(nouvelle_piece)
            self.log_promotion(nouvelle_piece)
            self.draw_board()
            self.update_status()
            popup.destroy()

        for cls, icon in [(Queen,"♛"), (Rook,"♜"), (Bishop,"♝"), (Knight,"♞")]:
            tk.Button(frame, text=icon, font=("Arial", 28), bg="#ecf0f1", bd=0, cursor="hand2", width=3, command=lambda c=cls: set_piece(c)).pack(side="left", padx=8)
        
        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)

    def update_status(self):
        game_result = self.chess.check_game_over()
        
        if game_result: 
            self.status_frame.config(bg="#e74c3c")
            self.status.config(text=" FIN DE PARTIE ", bg="#e74c3c", fg="white")
        elif self.chess.is_check(self.chess.current): 
            joueur = "Blancs" if self.chess.current == 0 else "Noirs"
            self.status_frame.config(bg="#e67e22")
            self.status.config(text=f" ÉCHEC ({joueur}) ", bg="#e67e22", fg="white")
        else: 
            if self.chess.current == 0:
                self.status_frame.config(bg="#ecf0f1")
                self.status.config(text=" Tour des Blancs ", bg="#ecf0f1", fg="#2c3e50")
            else:
                self.status_frame.config(bg="#2c3e50")
                self.status.config(text=" Tour des Noirs ", bg="#2c3e50", fg="white")

    def draw_victory_screen(self):
        game_result = self.chess.check_game_over()
        if not game_result: return
        
        c_size = 8 * self.square_size + 2 * self.margin
        self.canvas.create_rectangle(0, 0, c_size, c_size, fill="#000000", stipple="gray50")
        
        cy = c_size / 2
        if game_result == 'checkmate':
            winner = "Noirs" if self.chess.current == 0 else "Blancs"
            title, sub = "ÉCHEC ET MAT", f"Victoire des {winner}"
            color = "#27ae60"
        else:
            title, sub = "MATCH NUL", ""
            if game_result == 'stalemate_no_moves': sub = "Par Pat (aucun coup possible)"
            elif game_result == 'stalemate_material': sub = "Par matériel insuffisant"
            elif game_result == 'stalemate_repetition': sub = "Par répétition de la position"
            color = "#7f8c8d"
            
        self.canvas.create_rectangle(0, cy - 60, c_size, cy + 60, fill=color, outline="")
        self.canvas.create_rectangle(0, cy - 55, c_size, cy + 55, fill="#2c3e50", outline="")
        self.canvas.create_text(c_size / 2, cy - 15, text=title, font=("Helvetica", 32, "bold"), fill="white")
        self.canvas.create_text(c_size / 2, cy + 25, text=sub, font=("Helvetica", 16), fill="#bdc3c7")

    def save_game(self):
        f = filedialog.asksaveasfilename(defaultextension='.sav', filetypes=[("Sauvegarde Chess", "*.sav")])
        if f:
            with open(f, 'wb') as file: pickle.dump(self.chess, file)
            messagebox.showinfo('Sauvegarde', 'Partie sauvegardée avec succès !')

    def load_game(self):
        f = filedialog.askopenfilename(filetypes=[("Sauvegarde Chess", "*.sav")])
        if f:
            with open(f, 'rb') as file: self.chess = pickle.load(file)
            self.chess.board.chess = self.chess
            self.update_status()
            self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()