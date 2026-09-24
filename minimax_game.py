import math

class TicTacToeAI:
    def __init__(self):
        self.board = [' ' for _ in range(9)] # 3x3 board
        self.human_wins = 0
        self.ai_wins = 0
        self.draws = 0

    def print_board(self):
        print("\n")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")
        print("\n")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def check_winner(self, board, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for condition in win_conditions:
            if all([board[i] == player for i in condition]):
                return True
        return False

    # Minimax Algorithm for optimal decision-making[cite: 3]
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board, 'O'): # AI is 'O'
            return 1
        elif self.check_winner(board, 'X'): # Human is 'X'
            return -1
        elif not self.empty_squares():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.available_moves():
                board[move] = 'O'
                score = self.minimax(board, depth + 1, False)
                board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.available_moves():
                board[move] = 'X'
                score = self.minimax(board, depth + 1, True)
                board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        best_score = -math.inf
        best_move = None
        for move in self.available_moves():
            self.board[move] = 'O'
            score = self.minimax(self.board, 0, False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        self.board[best_move] = 'O'

    def human_move(self):
        valid_move = False
        while not valid_move:
            try:
                move = int(input("Enter your move (1-9): ")) - 1
                if move in self.available_moves():
                    self.board[move] = 'X'
                    valid_move = True
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def play_game(self):
        print("🤖 Welcome to AI Tic-Tac-Toe! You are 'X' and AI is 'O'.")
        print("Positions are numbered 1 to 9 (top-left to bottom-right).")
        
        while True:
            self.board = [' ' for _ in range(9)]
            
            while self.empty_squares():
                self.print_board()
                
                # Human Turn
                self.human_move()
                if self.check_winner(self.board, 'X'):
                    self.print_board()
                    print("🎉 You win! (Wait, that's impossible against Minimax!)")
                    self.human_wins += 1
                    break
                
                if not self.empty_squares():
                    self.print_board()
                    print("🤝 It's a Draw!")
                    self.draws += 1
                    break

                # AI Turn
                print("AI is making a move...")
                self.ai_move()
                if self.check_winner(self.board, 'O'):
                    self.print_board()
                    print("💻 AI Wins!")
                    self.ai_wins += 1
                    break
            
            # Track wins/losses[cite: 3]
            print(f"\nScoreboard -> You: {self.human_wins} | AI: {self.ai_wins} | Draws: {self.draws}")
            
            play_again = input("Do you want to play again? (y/n): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    game = TicTacToeAI()
    game.play_game()