import tkinter as tk
from tkinter import messagebox


class OthelloGame:
    def __init__(self):
        self.board = [[0] * 8 for _ in range(8)]
        self.board[3][3] = self.board[4][4] = 1  
        self.board[3][4] = self.board[4][3] = -1
        self.current_turn = 1  

    def make_move(self, row, col):
        if self.board[row][col] != 0 or not self.can_flip(row, col):
            return False

        player = self.current_player()

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        flipped = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            temp_flipped = []

            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -player:
                temp_flipped.append((r, c))
                r += dr
                c += dc

            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                flipped.extend(temp_flipped)

        if len(flipped) == 0:
            return False 

        self.board[row][col] = player
        for r, c in flipped:
            self.board[r][c] = player

        self.current_turn = -player  

        if not any(self.can_flip(r, c) for r in range(8) for c in range(8)):
            self.current_turn = -self.current_turn  

        return True

    def current_player(self):
        return self.current_turn

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False  

        return True

    def can_flip(self, row, col):
        if self.board[row][col] != 0:
            return False

        player = self.current_player()

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            flipped = False

            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == -player:
                    r += dr
                    c += dc
                elif self.board[r][c] == player and (r != row + dr or c != col + dc):
                    flipped = True
                    break
                else:
                    break

            if flipped:
                return True

        return False

    def update_board_ui(self):
        pass  

    def is_board_filled(self):
        for row in self.board:
            if 0 in row:
                return False  
        return True  

class OthelloGUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Othello Game")
        self.labels = [[None] * 8 for _ in range(8)]
        self.create_board()
        self.turn_label = tk.Label(self.window, text="", width=20, height=2)
        self.turn_label.grid(row=8, columnspan=8)

    def create_board(self):
        for row in range(8):
            for col in range(8):
                label = tk.Label(self.window, text=" ", width=4, height=2, relief="solid")
                label.grid(row=row, column=col)
                label.bind("<Button-1>", self.handle_click)
                self.labels[row][col] = label

    def update_board(self):
        for row in range(8):
            for col in range(8):
                cell_value = self.game.board[row][col]
                if cell_value == 1:
                    self.labels[row][col].config(text="●")
                elif cell_value == -1:
                    self.labels[row][col].config(text="〇")
                else:
                    self.labels[row][col].config(text=" ")
        self.update_turn_label() 
        if self.game.check_game_over():
            self.handle_game_over()

    def update_turn_label(self):
        current_player = self.game.current_player()
        if current_player == 1:
            self.turn_label.config(text="黒のターンです")
        else:
            self.turn_label.config(text="白のターンです")

    def handle_click(self, event):
        label = event.widget
        row, col = self.get_coordinates(label)

        if self.game.make_move(row, col):
            self.update_board()
        else:
            messagebox.showinfo("エラー", "石を置くことができません")

    def get_coordinates(self, label):
        for row in range(8):
            for col in range(8):
                if self.labels[row][col] == label:
                    return row, col

    def start(self):
        self.update_board()
        self.window.mainloop()

    def handle_game_over(self):
        white_count = sum(row.count(1) for row in self.game.board)
        black_count = sum(row.count(-1) for row in self.game.board)

        if white_count > black_count:
            message = "黒の勝利です！"
        elif black_count > white_count:
            message = "白の勝利です！"
        else:
            message = "引き分けです！"

        messagebox.showinfo("ゲーム終了", message)

        self.window.quit()  


game = OthelloGame()
gui = OthelloGUI(game)
gui.start()
