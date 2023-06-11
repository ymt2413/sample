import pygame
import random

pygame.init()

# ゲームウィンドウの設定
window_width = 300
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# 盤面の設定
play_width = 10
play_height = 20
block_size = window_width // play_width
grid = [[(0, 0, 0) for _ in range(play_width)] for _ in range(play_height)]

# テトロミノの設定
tetromino_shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]
tetromino_colors = [
    (255, 0, 0),     # 赤
    (0, 255, 0),     # 緑
    (0, 0, 255),     # 青
    (255, 255, 0),   # 黄色
    (255, 0, 255),   # ピンク
    (0, 255, 255),   # シアン
    (255, 165, 0)    # オレンジ
]

start_x = play_width // 2
start_y = 0

# テトロミノのクラス
class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(tetromino_shapes)
        self.color = random.choice(tetromino_colors)
        self.rotation = 0
        self.fall_time = pygame.time.get_ticks()

    def draw(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[0])):
                if self.shape[row][col]:
                    pygame.draw.rect(window, self.color, (self.x * block_size + col * block_size, self.y * block_size + row * block_size, block_size, block_size))

    def move_left(self):
        if self.x > 0 and not self.is_collision(-1, 0):
            self.x -= 1

    def move_right(self):
        if self.x < play_width - len(self.shape[0]) and not self.is_collision(1, 0):
            self.x += 1

    def is_collision(self, offset_x, offset_y):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[0])):
                if self.shape[row][col] and ((self.y + row + offset_y >= play_height) or
                                             (self.y + row + offset_y >= 0 and grid[(self.y + row + offset_y)][self.x + col + offset_x] != (0, 0, 0))):
                    return True
        return False

    def rotate(self):
        rotated_shape = [[self.shape[len(self.shape) - col - 1][row] for col in range(len(self.shape))] for row in range(len(self.shape[0]))]
        if self.x + len(rotated_shape[0]) <= play_width and not self.is_collision(0, 0):
            self.shape = rotated_shape
            self.rotation = (self.rotation + 1) % 4

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time >= 500:  # ブロックの落下速度を調整するにはここを変更してください
            self.fall_time = current_time
            if not self.is_collision(0, 1):
                self.y += 1
            else:
                self.lock_piece()
                game.check_lines()
                game.create_piece()
                if self.is_collision(0, 0):
                    game.game_over()

    def lock_piece(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[0])):
                if self.shape[row][col]:
                    grid[(self.y + row)][self.x + col] = self.color
        self.y = start_y

# ゲームのクラス
class Game:
    def __init__(self):
        self.piece = Tetromino(start_x, start_y)
        self.is_game_over = False

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.piece.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.piece.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.piece.update()
                    elif event.key == pygame.K_SPACE:
                        self.piece.rotate()

            self.update()
            self.draw()

        pygame.quit()

    def update(self):
        if not self.is_game_over:
            if not self.piece.is_collision(0, 1):
                self.piece.update()
            else:
                self.piece.lock_piece()
                self.check_lines()
                self.create_piece()
                if self.piece.is_collision(0, 0):
                    self.game_over()

    def draw(self):
        window.fill((0, 0, 0))  # 背景を黒でクリア
        for row in range(play_height):
            for col in range(play_width):
                pygame.draw.rect(window, (100, 100, 100), (col * block_size, row * block_size, block_size, block_size), 1)

        self.piece.draw()
        for row in range(play_height):
            for col in range(play_width):
                if grid[row][col] != (0, 0, 0):
                    pygame.draw.rect(window, grid[row][col], (col * block_size, row * block_size, block_size, block_size))

        pygame.display.update()

    def check_lines(self):
        full_lines = []
        for row in range(play_height):
            if all(grid[row]):
                full_lines.append(row)

        for full_line in full_lines:
            del grid[full_line]
            grid.insert(0, [(0, 0, 0) for _ in range(play_width)])

    def create_piece(self):
        self.piece = Tetromino(start_x, start_y)

    def game_over(self):
        self.is_game_over = True

# ゲームのインスタンスを作成して実行
game = Game()
game.run()
