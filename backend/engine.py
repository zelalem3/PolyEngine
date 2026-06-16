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
        self.move_log = []

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

    def make_move(self, move):
        """Executes a move on the board (updates array state)"""
        self.board[move.start_row][move.start_col] = "."
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """Reverts the last executed move"""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def check_pawn_move(self, piece, color, position, board):
        if color == "white":
            row_diff = position.start_row - position.end_row
            col_diff = abs(position.start_col - position.end_col)

            if row_diff <= 0:
                print("[!] Illegal Move!! Pawns can only move forward.")
                return False

            if col_diff == 0:
                if row_diff == 1:
                    if board[position.end_row][position.end_col] != ".":
                        print("[!] Illegal Move!! Blocked by another piece.")
                        return False
                    return True
                elif row_diff == 2:
                    if position.start_row != 6:
                        print("[!] Illegal Move!! Can only move 2 squares on the first move.")
                        return False
                    if board[position.start_row - 1][position.start_col] != "." or board[position.end_row][position.end_col] != ".":
                        print("[!] Illegal Move!! Path is blocked.")
                        return False
                    return True
                else:
                    print("[!] Illegal Move!! Pawns cannot move more than 2 squares.")
                    return False

            elif col_diff == 1 and row_diff == 1:
                target_piece = board[position.end_row][position.end_col]
                if target_piece == ".":
                    print("[!] Illegal Move!! Pawns can only move diagonally to capture.")
                    return False
                if target_piece.isupper():
                    print("[!] Illegal Move!! Cannot capture your own piece.")
                    return False
                return True
            else:
                print("[!] Illegal Move!! Invalid diagonal or horizontal movement layout.")
                return False

        elif color == "black":
            row_diff = position.end_row - position.start_row
            col_diff = abs(position.start_col - position.end_col)

            if row_diff <= 0:
                print("[!] Illegal Move!! Pawns can only move forward.")
                return False

            if col_diff == 0:
                if row_diff == 1:
                    if board[position.end_row][position.end_col] != ".":
                        print("[!] Illegal Move!! Blocked by another piece.")
                        return False
                    return True
                elif row_diff == 2:
                    if position.start_row != 1:
                        print("[!] Illegal Move!! Can only move 2 squares on the first move.")
                        return False
                    if board[position.start_row + 1][position.start_col] != "." or board[position.end_row][position.end_col] != ".":
                        print("[!] Illegal Move!! Path is blocked.")
                        return False
                    return True
                else:
                    print("[!] Illegal Move!! Pawns cannot move more than 2 squares.")
                    return False

            elif col_diff == 1 and row_diff == 1:
                target_piece = board[position.end_row][position.end_col]
                if target_piece == ".":
                    print("[!] Illegal Move!! Pawns can only move diagonally to capture.")
                    return False
                if target_piece.islower():
                    print("[!] Illegal Move!! Cannot capture your own piece.")
                    return False
                return True 
            else:
                print("[!] Illegal Move!! Invalid diagonal or horizontal movement layout.")
                return False
                
    def check_rook_move(self, color, position, board):
        if position.start_row != position.end_row and position.start_col != position.end_col:
            print("[!] Illegal Move!! Rooks can only move in straight lines.")
            return False

        row_step = 0 if position.start_row == position.end_row else (1 if position.end_row > position.start_row else -1)
        col_step = 0 if position.start_col == position.end_col else (1 if position.end_col > position.start_col else -1)

        curr_row = position.start_row + row_step
        curr_col = position.start_col + col_step

        while curr_row != position.end_row or curr_col != position.end_col:
            if board[curr_row][curr_col] != ".":
                print("[!] Illegal Move!! Path is blocked by a piece.")
                return False
            curr_row += row_step
            curr_col += col_step

        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper():
                print("[!] Illegal Move!! Cannot capture your own piece.")
                return False
            if color == "black" and target_piece.islower():
                print("[!] Illegal Move!! Cannot capture your own piece.")
                return False

        return True

    def check_bishop_move(self, color, position, board):
        row_diff = abs(position.start_row - position.end_row)
        col_diff = abs(position.start_col - position.end_col)

        if row_diff != col_diff:
            print("[!] Illegal Move!! Bishops can only move diagonally.")
            return False

        row_step = 1 if position.end_row > position.start_row else -1
        col_step = 1 if position.end_col > position.start_col else -1
        
        curr_row = position.start_row + row_step
        curr_col = position.start_col + col_step

        while curr_row != position.end_row and curr_col != position.end_col:
            if board[curr_row][curr_col] != ".":
                print("[!] Illegal Move!! The diagonal path is blocked.")
                return False
            curr_row += row_step
            curr_col += col_step
        
        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper():
                print("[!] Illegal Move!!! Cannot capture your own piece.")
                return False                
            if color == "black" and target_piece.islower():
                print("[!] Illegal Move!!! Cannot capture your own piece.")
                return False                

        return True
    
    def check_knight_move(self, color, position, board):
        row_diff = abs(position.start_row - position.end_row)
        col_diff = abs(position.start_col - position.end_col)

        # 1. If it's NOT a valid L-shape, it's illegal
        if row_diff * col_diff != 2:
            print("[!] Illegal Move!!! Knights must move in an L-shape.")
            return False
        
        # 2. Check the landing square for friendly pieces
        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper():
                print("[!] Illegal Move!!! Cannot capture your own piece.")
                return False
            if color == "black" and target_piece.islower():
                print("[!] Illegal Move!!! Cannot capture your own piece.")
                return False
        
        return True
    
    def check_king_move(self, color, position, board):
        row_diff = abs(position.start_row - position.end_row)
        col_diff = abs(position.start_col - position.end_col)

        if row_diff > 1 or col_diff > 1:
            print("[!] Illegal Move!!! The King can only move one square.")
            return False

        if row_diff == 0 and col_diff == 0:
            print("[!] Illegal Move!!! You must move to a different square.")
            return False

        target_piece = board[position.end_row][position.end_col]
        if target_piece != ".":
            if color == "white" and target_piece.isupper():
                print("[!] Illegal Move!!! Cannot capture your own piece.")
                return False
            if color == "black" and target_piece.islower():
                print("[!] Illegal Move!!! Cannot capture your own piece.")
                return False

        enemy_king = "k" if color == "white" else "K"

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                check_row = position.end_row + dr
                check_col = position.end_col + dc

                if 0 <= check_row < 8 and 0 <= check_col < 8:
                    if board[check_row][check_col] == enemy_king:
                        print("[!] Illegal Move!!! Kings cannot stand adjacent to each other.")
                        return False

        return True


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
        game.print_board()
        turn_text = "White" if game.white_to_move else "Black"
        user_input = input(f"[{turn_text}'s Turn] Enter command: ").strip().lower()

        if user_input == 'quit':
            print("Exiting engine simulator. Goodbye!")
            break
            
        if user_input == 'undo':
            if len(game.move_log) > 0:
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

            moving_piece = game.board[start_sq[0]][start_sq[1]]
            if moving_piece == ".":
                print("[!] There is no piece on your selected starting square!")
                continue

            # Enforce Turn Order
            if game.white_to_move and moving_piece.islower():
                print("[!] Illegal Move!! It is White's turn.")
                continue
            if not game.white_to_move and moving_piece.isupper():
                print("[!] Illegal Move!! It is Black's turn.")
                continue

            move = Move(start_sq, end_sq, game.board)
            piece_type = moving_piece.lower()
            color = "white" if moving_piece.isupper() else "black"

            # Route to validation engine handlers
            is_legal = False
            if piece_type == "p":
                is_legal = game.check_pawn_move(piece_type, color, move, game.board)
            elif piece_type == "r":
                is_legal = game.check_rook_move(color, move, game.board)
            elif piece_type == "b":
                is_legal = game.check_bishop_move(color, move, game.board)
            elif piece_type == "k":
                is_legal = game.check_king_move(color, move, game.board)
            elif piece_type == "q":
                # A Queen is mathematically just a Rook combined with a Bishop!
                is_legal = game.check_rook_move(color, move, game.board) or game.check_bishop_move(color, move, game.board)
            elif piece_type == "n":
                # Fallback allowance until Knight offsets are programmed
                is_legal = True

            if is_legal:
                game.make_move(move)
                print(f"[*] Moved: {move.get_chess_notation().upper()}")

        except (KeyError, IndexError):
            print("[!] Invalid squares. Stay within the a1 to h8 boundary.")