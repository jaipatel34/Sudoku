import pygame
from sudoku_generator import SudokuGenerator

# Pygame initialization and window setup
pygame.init()
WIDTH = 540
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Set up colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("comicsansms", 40)

# Sudoku board generation
size = 9
removed = 30  # Adjust the number of removed cells as needed
sudoku = SudokuGenerator(size, removed)
sudoku.fill_values()
board = sudoku.get_board()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    WINDOW.fill(WHITE)

    # Draw the Sudoku grid and numbers
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(WINDOW, BLACK, (j * 60, i * 60, 60, 60), 1)  # Corrected x, y coordinates
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, BLACK)
                WINDOW.blit(text, (j * 60 + 20, i * 60 + 20))  # Corrected x, y coordinates

    # Update the display
    pygame.display.update()

pygame.quit()
