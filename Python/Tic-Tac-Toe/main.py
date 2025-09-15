"""
Author:         Jake Bredice
Date:           11-11-2024
Assignment:     Project 1: Tic-Tac-Toe
Course:         CPSC1051
Lab Section:    SECTION 001

CODE DESCRIPTION:
Tic Tac Toe Game
"""
class TicTacToeBoard:
    def __init__(self):
        # Initialize a blank 3x3 board
        self.board = [["_"] * 3 for _ in range(3)]
        self.current_player = "X"
    def displayboard(self):
        """
        Displays current board
        Args:
            self
        Returns:
            prints board
        """
        for row in self.board:
            print("| " + " | ".join(row) + " |")
    def updateboard(self, row, col):
        """
        Validates input and updates board
        Args:
            self
            row: int that has already been checked to be a digit
            col: int that has already been checked to be a digit
        Returns:
            False if inputs are out of bounds or spot is filled
            True if inputs are valid and board succesfully updates
        """
        
        # Check bounds
        if not (0 <= row < 3 and 0 <= col < 3):
            print("Please enter valid row and col numbers from 1 to 3:")
            return False
        # Check filled
        if self.board[row][col] != "_":
            print("That spot is full!")
            print("Please enter valid row and col numbers from 1 to 3:")
            return False
        # Update board if move is valid
        self.board[row][col] = self.current_player
        return True
    def switchplayer(self):
        """
        Switches current player
        Args:
            self
        Returns:
            none, switches player
        """
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
    def promptmove(self):
        """
        Displays current board and validates if input is 2 integers
        Args:
            self
        Returns:
            none
        """
        print(f"Enter row and column for player {self.current_player}")
        while True:
            move = input().strip()
            parts = move.split()
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                row = int(parts[0]) - 1
                col = int(parts[1]) - 1
                if self.updateboard(row, col):
                    break  # Valid move, exit the loop
            else:
                print("Please enter valid row and col numbers from 1 to 3:")
                
    def checkover(self):
        """
        Checks for win
        Args:
            self
        Returns:
            True and method of winning or tie if game is over
            False and '' if not
        """
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "_":
                return True, f"Player {self.board[i][0]} WINS!"
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "_":
                return True, f"Player {self.board[0][i]} WINS!"
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "_":
            return True, f"Player {self.board[0][0]} WINS!"
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "_":
            return True, f"Player {self.board[0][2]} WINS!"
        
        # Check for tie
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "_":
                    return False, '' 
        return True, 'It\'s a TIE!'
        
    def promptagain(self):
        """
        Prompt the user to play again
        Args:
            self
        Returns:
            True if playing again
            False if not
            
        """
        while True:
            print("\nDo you want to play again? Y or N")
            play_again = input().strip().upper()
            if play_again in ['Y', 'N']:
                return play_again == 'Y'
            print("Please enter valid input: Y or N")
        
        return False
def play():
# Main game loop
    while True:
        print("Let's play Tic-Tac-Toe!")
        print("When prompted, enter desired row and column numbers")
        print("Example: 1 3")
        game = TicTacToeBoard()
        game.board[0][2] = 'X'
        game.displayboard()
        game.board[0][2] = '_'
        print("Let's play!")
        print('Player X starts!')
        game.displayboard()
        
        while True:
            # Prompt player to make a move
            game.promptmove()
            game.displayboard()

            # Check if the game is over
            game_over, result = game.checkover()
            if game_over:
                print(result)
                break  # End the game loop
        
            # Switch players
            game.switchplayer()

        # Ask if they want to play again
        if not game.promptagain():
            print("Thanks for playing!")
            break  # Exit the game loop
if __name__ == "__main__":
    play()
