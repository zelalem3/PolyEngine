import subprocess

class GameState:
    def __init__(self):
        # The board is an 8x8 2D list. 
        # White pieces are uppercase, Black pieces are lowercase, '.' is empty.
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.white_to_move = True
        self.white_king_location = (7, 4)  
        self.black_king_location = (0, 4)
        self.move_log = []

    def ask_stockfish_for_move(self):
        """Communicates directly with the system Stockfish binary using raw UCI strings."""
        played_moves = " ".join([move.get_chess_notation() for move in self.move_log])
        
        try:
            # Open up a direct pipestream straight to your Ubuntu apt-installed binary
            engine = subprocess.Popen(
                "/usr/games/stockfish",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send standard UCI commands: feed the history, calculate for 500ms, then quit
            uci_commands = f"position startpos moves {played_moves}\ngo movetime 500\nquit\n"
            output, _ = engine.communicate(input=uci_commands)
            
            # Parse the text block line by line to locate the action command
            for line in output.split("\n"):
                if line.startswith("bestmove"):
                    # Extract 'e7e5' out of "bestmove e7e5 ponder d2d4"
                    return line.split()[1]
        except Exception as e:
            print(f"[!] Engine subprocess error: {e}")
            
        return None

    def print_board(self):
        """Prints a clean, readable version of the board to the terminal."""
        print("\n  a b c d e f g h")
        print("  ---------------")
        for i, row in enumerate(self.board):
            rank = 8 - i
            row_string = " ".join(row)
            print(f"{rank}|{row_string}|{rank}")
        print("  ---------------")
        print("  a b c d e f g h\n")

    def get_all_possible_moves(self):
        """Generates all raw moves based strictly on piece physics (geometry)."""
        possible_moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == ".":
                    continue
                
                color = "white" if piece.isupper() else "black"
                if (color == "white" and not self.white_to_move) or (color == "black" and self.white_to_move):
                    continue
                
                for target_r in range(8):
                    for target_col in range(8):
                        from_sq = (r, c)
                        to_sq = (target_r, target_col)
                        move = Move(from_sq, to_sq, self.board)
                        
                        piece_type = piece.lower()
                        is_legal = False
                        
                        if piece_type == "p":
                            is_legal = self.check_pawn_move(piece_type, color, move, self.board)
                        elif piece_type == "r":
                            is_legal = self.check_rook_move(color, move, self.board)
                        elif piece_type == "b":
                            is_legal = self.check_bishop_move(color, move, self.board)
                        elif piece_type == "n":
                            is_legal = self.check_knight_move(color, move, self.board)
                        elif piece_type == "k":
                            is_legal = self.check_king_move(color, move, self.board)
                        elif piece_type == "q":
                            is_legal = self.check_rook_move(color, move, self.board) or self.check_bishop_move(color, move, self.board)
                            
                        if is_legal:
                            possible_moves.append(move)
        return possible_moves

    def get_valid_moves(self):
        """Filters out all moves that leave your own king in check."""
        possible_moves = self.get_all_possible_moves()
        valid_moves = []
        
        for move in possible_moves:
            self.make_move(move)
            self.white_to_move = not self.white_to_move
            
            if not self.in_check():
                valid_moves.append(move)
                
            self.white_to_move = not self.white_to_move
            self.undo_move()
            
        return valid_moves
        
    def in_check(self):
        """Determines if the player whose turn it currently is is in check."""
        if self.white_to_move:
            return self.check_validation("white", self.white_king_location, self.board)
        else:
            return self.check_validation("black", self.black_king_location, self.board)

    def make_move(self, move):
        """Executes a move on the board (updates array state)"""
        self.board[move.start_row][move.start_col] = "."
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        
        if move.piece_moved == "K":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "k":
            self.black_king_location = (move.end_row, move.end_col)
            
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """Reverts the last executed move"""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            
            if move.piece_moved == "K":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "k":
                self.black_king_location = (move.start_row, move.start_col)

    def check_pawn_move(self, piece, color, position, board):
        if color == "white":
            row_diff = position.start_row - position.end_row
            col_diff = abs(position.start_col - position.end_col)

            if row_diff <= 0:
                return False
            if col_diff == 0:
                if row_diff == 1:
                    return board[position.end_row][position.end_col] == "."
                elif row_diff == 2:
                    if position.start_row != 6:
                        return False
                    return board[position.start_row - 1][position.start_col] == "." and board[position.end_row][position.end_col] == "."
                return False
            elif col_diff == 1 and row_diff == 1:
                target_piece = board[position.end_row][position.end_col]
                return target_piece != "." and target_piece.islower()
            return False

        elif color == "black":
            row_diff = position.end_row - position.start_row
            col_diff = abs(position.start_col - position.end_col)

            if row_diff <= 0:
                return False
            if col_diff == 0:
                if row_diff == 1:
                    return board[position.end_row][position.end_col] == "."
                elif row_diff == 2:
                    if position.start_row != 1:
                        return False
                    return board[position.start_row + 1][position.start_col] == "." and board[position.end_row][position.end_col] == "."
                return False
            elif col_diff == 1 and row_diff == 1:
                target_piece = board[position.end_row][position.end_col]
                return target_piece != "." and target_piece.isupper()
            return False
                
    def check_rook_move(self, color, position, board):
        if position.start_row != position.end_row and position.start_col != position.end_col:
            return False

        row_step = 0 if position.start_row == position.end_row else (1 if position.end_row > position.start_row else -1)
        col_step = 0 if position.start_col == position.end_col else (1 if position.end_col > position.start_col else -1)

        curr_row = position.start_row + row_step
        curr_col = position.start_col + col_step

        while curr_row != position.end_row or curr_col != position.end_col:
            if board[curr_row][curr_col] != ".":
                return False
            curr_row += row_step
            curr_col += col_step

        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper(): return False
            if color == "black" and target_piece.islower(): return False

        return True

    def check_bishop_move(self, color, position, board):
        row_diff = abs(position.start_row - position.end_row)
        col_diff = abs(position.start_col - position.end_col)

        if row_diff != col_diff:
            return False

        row_step = 1 if position.end_row > position.start_row else -1
        col_step = 1 if position.end_col > position.start_col else -1
        
        curr_row = position.start_row + row_step
        curr_col = position.start_col + col_step

        while curr_row != position.end_row and curr_col != position.end_col:
            if board[curr_row][curr_col] != ".":
                return False
            curr_row += row_step
            curr_col += col_step
        
        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper(): return False                
            if color == "black" and target_piece.islower(): return False                

        return True
    
    def check_knight_move(self, color, position, board):
        row_diff = abs(position.start_row - position.end_row)
        col_diff = abs(position.start_col - position.end_col)

        if row_diff * col_diff != 2:
            return False
        
        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper(): return False
            if color == "black" and target_piece.islower(): return False
        
        return True
    
    def check_king_move(self, color, position, board):
        row_diff = abs(position.start_row - position.end_row)
        col_diff = abs(position.start_col - position.end_col)

        if row_diff > 1 or col_diff > 1:
            return False
        if row_diff == 0 and col_diff == 0:
            return False

        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper(): return False
            if color == "black" and target_piece.islower(): return False

        enemy_king = "k" if color == "white" else "K"

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                check_row = position.end_row + dr
                check_col = position.end_col + dc
                if 0 <= check_row < 8 and 0 <= check_col < 8:
                    if board[check_row][check_col] == enemy_king:
                        return False
        return True

    def check_validation(self, color, square, board):
        start_row, start_col = square[0], square[1]
        
        if color == "white":
            enemy_rook, enemy_bishop, enemy_queen, enemy_knight, enemy_pawn = "r", "b", "q", "n", "p"
            pawn_row_offsets, pawn_col_offsets = [-1, -1], [-1, 1]
        else:
            enemy_rook, enemy_bishop, enemy_queen, enemy_knight, enemy_pawn = "R", "B", "Q", "N", "P"
            pawn_row_offsets, pawn_col_offsets = [1, 1], [-1, 1]

        # Straight lines
        straight_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in straight_directions:
            curr_row, curr_col = start_row + dr, start_col + dc
            while 0 <= curr_row < 8 and 0 <= curr_col < 8:
                target_piece = board[curr_row][curr_col]
                if target_piece == ".":
                    curr_row += dr
                    curr_col += dc
                else:
                    if target_piece == enemy_rook or target_piece == enemy_queen: return True
                    break

        # Diagonals
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in diagonal_directions:
            curr_row, curr_col = start_row + dr, start_col + dc
            while 0 <= curr_row < 8 and 0 <= curr_col < 8:
                target_piece = board[curr_row][curr_col]
                if target_piece == ".":
                    curr_row += dr
                    curr_col += dc
                else:
                    if target_piece == enemy_bishop or target_piece == enemy_queen: return True
                    break

        # Knights
        knight_offsets = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2)]
        for dr, dc in knight_offsets:
            check_row, check_col = start_row + dr, start_col + dc
            if 0 <= check_row < 8 and 0 <= check_col < 8:
                if board[check_row][check_col] == enemy_knight: return True

        # Pawns
        for i in range(2):
            check_row = start_row + pawn_row_offsets[i]
            check_col = start_col + pawn_col_offsets[i]
            if 0 <= check_row < 8 and 0 <= check_col < 8:
                if board[check_row][check_col] == enemy_pawn: return True

        return False                


class Move:
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
    ranks_to_rows = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __eq__(self, other):
        """Enables object comparison inside our legal moves verification step"""
        if isinstance(other, Move):
            return (self.start_row == other.start_row and self.start_col == other.start_col and
                    self.end_row == other.end_row and self.end_col == other.end_col)
        return False


if __name__ == "__main__":
    game = GameState()
    files_to_cols = Move.files_to_cols
    ranks_to_rows = Move.ranks_to_rows
    
    print("==================================================")
    print("      Welcome to Centipawn Terminal Mode Engine   ")
    print("==================================================")
    print("Instructions:")
    print("  - Move format: Type 'start square' then 'end square' (e.g., e2e4)")
    print("  - Type 'undo' to revert the last move.")
    print("  - Type 'quit' to exit.")

    while True:
        # Pre-calculate legal paths at the start of the turn
        valid_moves = game.get_valid_moves()
        
        # Check for Game Over conditions
        if len(valid_moves) == 0:
            if game.in_check():
                print(f"\n[!!!] CHECKMATE! {'Black' if game.white_to_move else 'White'} wins!")
            else:
                print("\n[---] STALEMATE! The game ends in a draw.")
            break

        game.print_board()
        
        if game.in_check():
            print("[!] WARNING: King is currently in CHECK!")

        # --- AUTOMATIC STOCKFISH AI LOOP FOR BLACK ---
        if not game.white_to_move:
            print("[*] Stockfish is thinking...")
            ai_move_string = game.ask_stockfish_for_move()
            
            if ai_move_string:
                # Extract coordinates from Stockfish's notation output
                start_file, start_rank = ai_move_string[0], ai_move_string[1]
                end_file, end_rank = ai_move_string[2], ai_move_string[3]

                start_sq = (ranks_to_rows[start_rank], files_to_cols[start_file])
                end_sq = (ranks_to_rows[end_rank], files_to_cols[end_file])

                ai_move_object = Move(start_sq, end_sq, game.board)
                
                # Check calculation safety against custom engine layout logic
                if ai_move_object in valid_moves:
                    game.make_move(ai_move_object)
                    print(f"[#] Stockfish played: {ai_move_string.upper()}")
                else:
                    print(f"[!] Warning: Stockfish suggested a move ({ai_move_string.upper()}) your engine flagged as invalid.")
                    print("Executing anyway to sync state...")
                    game.make_move(ai_move_object)
            else:
                print("[!] Stockfish returned no moves. Ending match.")
                break
            continue

        # --- STANDARD HUMAN LOOP FOR WHITE ---
        user_input = input("[White's Turn] Enter command: ").strip().lower()

        if user_input == 'quit':
            print("Exiting engine simulator. Goodbye!")
            break
            
        if user_input == 'undo':
            # Undo twice so it goes back to your previous turn (undoes AI move + your move)
            if len(game.move_log) >= 2:
                game.undo_move()
                game.undo_move()
                print("[*] Undid your move and Stockfish's counter-move.")
            elif len(game.move_log) == 1:
                game.undo_move()
                print("[*] Undid last move.")
            else:
                print("[!] No moves left to undo!")
            continue

        if len(user_input) != 4:
            print("[!] Invalid format. Please use coordinate format like 'e2e4'.")
            continue

        try:
            start_file, start_rank = user_input[0], user_input[1]
            end_file, end_rank = user_input[2], user_input[3]

            start_sq = (ranks_to_rows[start_rank], files_to_cols[start_file])
            end_sq = (ranks_to_rows[end_rank], files_to_cols[end_file])

            # Construct the user's intent object
            user_move = Move(start_sq, end_sq, game.board)

            # --- Check Against the Safe Valid Moves List ---
            if user_move in valid_moves:
                game.make_move(user_move)
                print(f"[*] Moved: {user_move.get_chess_notation().upper()}")
            else:
                print("[!] Illegal Move!! That move is either geometric friction or leaves your king in check.")

        except (KeyError, IndexError):
            print("[!] Invalid squares. Stay within the a1 to h8 boundary.")