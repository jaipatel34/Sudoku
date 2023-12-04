import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 20)

# Sudoku board and difficulty levels
board = [[0 for _ in range(9)] for _ in range(9)]
difficulty = None
empty_cells = {
    "easy": 30,
    "medium": 40,
    "hard": 50
}
selected_row, selected_col = -1, -1

# Functions
def draw_board():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (50, 50, 450, 450), 2)

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j * 50 + 65, i * 50 + 58))

    for i in range(10):
        if i % 3 == 0:
            thickness = 2
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (50 + i * 50, 50), (50 + i * 50, 500), thickness)
        pygame.draw.line(screen, BLACK, (50, 50 + i * 50), (500, 50 + i * 50), thickness)

def generate_board(diff):
    global board
    board = [[random.randint(1, 9) for _ in range(9)] for _ in range(9)]
    for _ in range(empty_cells[diff]):
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_buttons():
    pygame.draw.rect(screen, GRAY, (160, 240, 220, 50))
    pygame.draw.rect(screen, GRAY, (160, 320, 220, 50))
    pygame.draw.rect(screen, GRAY, (160, 400, 220, 50))
    draw_text('Easy', font, BLACK, 250, 250)
    draw_text('Medium', font, BLACK, 230, 330)
    draw_text('Hard', font, BLACK, 250, 410)

def draw_start_screen():
    screen.fill(WHITE)
    draw_text('Select Difficulty:', font, BLACK, 50, 50)
    draw_buttons()
    pygame.display.flip()

def main():
    global difficulty, selected_row, selected_col
    running = True
    difficulty_selected = False

    while running:
        draw_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 160 <= mouse_pos[0] <= 380 and 240 <= mouse_pos[1] <= 290:
                    difficulty = "easy"
                    difficulty_selected = True
                elif 160 <= mouse_pos[0] <= 380 and 320 <= mouse_pos[1] <= 370:
                    difficulty = "medium"
                    difficulty_selected = True
                elif 160 <= mouse_pos[0] <= 380 and 400 <= mouse_pos[1] <= 450:
                    difficulty = "hard"
                    difficulty_selected = True

        if difficulty_selected:
            generate_board(difficulty)
            difficulty_selected = False
            selected_row, selected_col = -1, -1

        draw_board()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
