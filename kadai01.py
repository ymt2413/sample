import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()


width = 600
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("〇×ゲーム")

running = True


board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

def draw_board():
    screen.fill((255, 255, 255)) 

    cell_width = width // 3
    cell_height = height // 3

    for row in range(3):
        for col in range(3):
            cell_x = col * cell_width
            cell_y = row * cell_height

            pygame.draw.rect(screen, (0, 0, 0), (cell_x, cell_y, cell_width, cell_height), 1)  # セルの枠を描画

            symbol = board[row][col]
            if symbol is not None:
                font = pygame.font.Font(None, 100)
                text = font.render(symbol, True, (0, 0, 0))
                text_rect = text.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                screen.blit(text, text_rect) 

    pygame.display.update()

def handle_player_input():
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        mouse_pos = pygame.mouse.get_pos()
        cell_x = mouse_pos[0] // (width // 3)
        cell_y = mouse_pos[1] // (height // 3)
        if board[cell_y][cell_x] is None and not game_over:
            board[cell_y][cell_x] = current_player
            check_game_over()
            if not game_over:
                change_player()

def check_game_over():
    global game_over

 
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
          
            show_message_box(f"勝者: {row[0]}")
            game_over = True
            return

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
           
            show_message_box(f"勝者: {board[0][col]}")
            game_over = True
            return

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        show_message_box(f"勝者: {board[0][0]}")
        game_over = True
        return

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        show_message_box(f"勝者: {board[0][2]}")
        game_over = True
        return

    is_board_full = all(all(cell is not None for cell in row) for row in board)
    if is_board_full:
        show_message_box("引き分け")
        game_over = True
        return

def show_message_box(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("ゲーム終了", message)
    root.destroy()

def change_player():
    global current_player
    current_player = "〇" if current_player == "×" else "×"

current_player = "〇"
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_player_input()
    draw_board()

    pygame.display.update()
