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
            # 8 minus index gives us the correct chess rank numbers (8 down to 1)
            rank = 8 - i
            row_string = " ".join(row)
            print(f"{rank}|{row_string}|{rank}")
        print("  ---------------")
        print("  a b c d e f g h\n")

    def make_move(self, move):
        """Executes a move on the board (updates array state)"""
        # Clear the starting square
        self.board[move.start_row][move.start_col] = "."
        # Place the piece on the destination square
        self.board[move.end_row][move.end_col] = move.piece_moved
        # Log the move and swap turns
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """Reverts the last executed move"""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move


class Move:
    # Map chess notation files/ranks to array rows/columns
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
        """Returns standard coordinate notation like 'e2e4'"""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
    



# Interactive loop runner
if __name__ == "__main__":
    game = GameState()
    
    # Helper dictionary to quickly turn terminal text input (like 'e2') into array indices (row, col)
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    ranks_to_rows = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}

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

        # Basic input validation for coordinate moves (e.g., e2e4 is 4 characters long)
        if len(user_input) != 4:
            print("[!] Invalid format. Please use coordinate format like 'e2e4'.")
            continue

        try:
            start_file, start_rank = user_input[0], user_input[1]
            end_file, end_rank = user_input[2], user_input[3]

            # Convert human algebraic notation to our internal 2D array coordinates
            start_sq = (ranks_to_rows[start_rank], files_to_cols[start_file])
            end_sq = (ranks_to_rows[end_rank], files_to_cols[end_file])

            # Check if there is actually a piece at the starting square
            if game.board[start_sq[0]][start_sq[1]] == ".":
                print("[!] There is no piece on your selected starting square!")
                continue

            # Execute the move manually
            move = Move(start_sq, end_sq, game.board)
            game.make_move(move)
            print(f"[*] Moved: {move.get_chess_notation().upper()}")

        except (KeyError, IndexError):
            print("[!] Invalid squares. Stay within the a1 to h8 boundary.")