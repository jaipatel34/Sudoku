'''from sudoku_generator import SudokuGenerator
import pygame


WIDTH = 550
background_color = (255, 255, 255)



def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Sudoku')
    #win.fill((236, 231, 261))
    for i in range(0,10):
        if i%3 == 0:
            pygame.draw.line(win, (236,236,236), (50 + 50 * i,50), (50 + 50 * i,500), 4)
            pygame.draw.line(win, (236,236,236), (50 , 50 + 50 * i), (500, 50 + 50 * i), 4)
        pygame.draw.line(win, (236,236,236), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, (236,236,236), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__=="__main__":
    size = 9
    removed = 80
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    print(board)
    main()'''

import pygame
import random
from sudoku_generator import SudokuGenerator

WIDTH = 550
BACKGROUND_COLOR = (236, 231, 213)
GRID_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)

class DifficultyButton:
    def __init__(self, text, rect, color, text_position):
        self.text = text
        self.rect = rect
        self.color = color
        self.text_position = text_position

class GameButton:
    def __init__(self, text, rect, color, text_position, action):
        self.text = text
        self.rect = rect
        self.color = color
        self.text_position = text_position
        self.action = action

def draw_grid(win, sudoku, selected):
    win.fill(BACKGROUND_COLOR)

    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, GRID_COLOR, (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(win, GRID_COLOR, (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
        pygame.draw.line(win, GRID_COLOR, (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, GRID_COLOR, (50, 50 + 50 * i), (500, 50 + 50 * i), 2)

    font = pygame.font.Font(None, 36)
    for i in range(9):
        for j in range(9):
            x, y = 70 + j * 50, 70 + i * 50
            rect = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(win, SELECTED_COLOR if (i, j) == selected else BACKGROUND_COLOR, rect)

            if sudoku.get_board()[i][j] != 0:
                text = font.render(str(sudoku.get_board()[i][j]), True, FONT_COLOR)
                win.blit(text, (x + 15, y + 15))

def draw_buttons(win, buttons):
    button_font = pygame.font.Font(None, 36)

    for button in buttons:
        pygame.draw.rect(win, button.color, button.rect)
        text = button_font.render(button.text, True, FONT_COLOR)
        win.blit(text, button.text_position)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Sudoku')

    start_screen_buttons = [
        DifficultyButton("Easy", pygame.Rect(200, 200, 150, 50), (0, 255, 0), (220, 215)),
        DifficultyButton("Medium", pygame.Rect(200, 300, 150, 50), (255, 255, 0), (205, 315)),
        DifficultyButton("Hard", pygame.Rect(200, 400, 150, 50), (255, 0, 0), (225, 415)),
    ]

    game_screen_buttons = [
        GameButton("Reset", pygame.Rect(50, 520, 100, 30), (0, 0, 255), (70, 525), "reset"),
        GameButton("Restart", pygame.Rect(180, 520, 100, 30), (255, 165, 0), (185, 525), "restart"),
        GameButton("Exit", pygame.Rect(310, 520, 100, 30), (255, 0, 0), (330, 525), "exit"),
    ]

    selected_difficulty = None
    selected_cell = None

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if selected_difficulty:
                    for button in game_screen_buttons:
                        if button.rect.collidepoint(pos):
                            if button.action == "reset":
                                # Implement the reset action
                                print("Reset clicked")
                            elif button.action == "restart":
                                # Implement the restart action
                                print("Restart clicked")
                            elif button.action == "exit":
                                run = False
                else:
                    for button in start_screen_buttons:
                        if button.rect.collidepoint(pos):
                            selected_difficulty = button.text
                            size = 9
                            removed = 30  # Default to easy difficulty
                            if selected_difficulty == "Medium":
                                removed = 40
                            elif selected_difficulty == "Hard":
                                removed = 50
                            sudoku = SudokuGenerator(size, removed)
                            sudoku.fill_values()
                            sudoku.remove_cells()
                if selected_difficulty:
                    selected_cell = ((pos[1] - 50) // 50, (pos[0] - 50) // 50)

        if selected_difficulty:
            draw_grid(win, sudoku, selected_cell)
            draw_buttons(win, game_screen_buttons)
        else:
            win.fill(BACKGROUND_COLOR)
            draw_buttons(win, start_screen_buttons)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()


