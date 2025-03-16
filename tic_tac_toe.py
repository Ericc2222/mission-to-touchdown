import tkinter as tk
from tkinter import messagebox
import sys

def main():
    try:
        print("Starting Tic Tac Toe game...")
        game = TicTacToe()
        print("Game initialized, launching window...")
        game.run()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

class TicTacToe:
    def __init__(self):
        try:
            self.window = tk.Tk()
            self.window.title("Tic Tac Toe with B's and C's")
            
            # Make window appear on top
            self.window.lift()
            self.window.attributes('-topmost', True)
            
            # Set window background color
            self.window.configure(bg='lightblue')
            
            # Set minimum window size
            self.window.minsize(300, 400)
            
            # Game state
            self.current_player = "B"
            self.board = [[" " for _ in range(3)] for _ in range(3)]
            self.buttons = []
            
            # Create status label
            self.status_label = tk.Label(
                self.window,
                text=f"Player {self.current_player}'s turn",
                font=('Arial', 15),
                bg='lightblue'
            )
            self.status_label.grid(row=0, column=0, columnspan=3, pady=10)
            
            # Create game board buttons
            for i in range(3):
                row_buttons = []
                for j in range(3):
                    button = tk.Button(
                        self.window,
                        text=" ",
                        font=('Arial', 20, 'bold'),
                        width=5,
                        height=2,
                        bg='white',
                        command=lambda row=i, col=j: self.button_click(row, col)
                    )
                    button.grid(row=i+1, column=j, padx=5, pady=5)
                    row_buttons.append(button)
                self.buttons.append(row_buttons)
            
            # Create restart button
            restart_button = tk.Button(
                self.window,
                text="Restart Game",
                font=('Arial', 12),
                bg='lightgreen',
                command=self.restart_game
            )
            restart_button.grid(row=4, column=0, columnspan=3, pady=10)
            
            # Center the window on the screen
            self.window.update_idletasks()
            width = self.window.winfo_width()
            height = self.window.winfo_height()
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f'{width}x{height}+{x}+{y}')
            
            # After a short delay, remove topmost attribute
            self.window.after(1000, lambda: self.window.attributes('-topmost', False))
            
            print("Window created successfully")
            
        except Exception as e:
            print(f"Error in initialization: {str(e)}")
            raise
    
    def button_click(self, row, col):
        try:
            # Check if the cell is empty
            if self.board[row][col] == " ":
                # Update board and button
                self.board[row][col] = self.current_player
                self.buttons[row][col].config(text=self.current_player)
                
                # Check for winner
                if self.check_winner(self.current_player):
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                    self.restart_game()
                    return
                
                # Check for tie
                if self.is_board_full():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.restart_game()
                    return
                
                # Switch player
                self.current_player = "C" if self.current_player == "B" else "B"
                self.status_label.config(text=f"Player {self.current_player}'s turn")
        except Exception as e:
            print(f"Error in button click: {str(e)}")
    
    def check_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_board_full(self):
        return all(cell != " " for row in self.board for cell in row)
    
    def restart_game(self):
        try:
            # Reset game state
            self.current_player = "B"
            self.board = [[" " for _ in range(3)] for _ in range(3)]
            
            # Reset buttons
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(text=" ")
            
            # Reset status label
            self.status_label.config(text=f"Player {self.current_player}'s turn")
        except Exception as e:
            print(f"Error in restart game: {str(e)}")
    
    def run(self):
        try:
            print("Starting main event loop...")
            self.window.mainloop()
            print("Main event loop ended")
        except Exception as e:
            print(f"Error in main loop: {str(e)}")

if __name__ == "__main__":
    main()

    