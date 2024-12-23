from sudoku_generator import SudokuGenerator, Board, Cell
from sudoku_generator import *
import pygame
import random
import math

WIDTH = 600
BACKGROUND_COLOR = (255, 255, 255)
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

def draw_grid(win, sudoku, selected, sketch_mode, selected_number):
    win.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 36)
    sketch_font = pygame.font.Font(None, 20)

    for i in range(9):
        for j in range(9):
            x, y = 70 + j * 50, 70 + i * 50
            rect = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(win, SELECTED_COLOR if (i, j) == selected else BACKGROUND_COLOR, rect)

            cell_value = sudoku.get_board()[i][j]
            if cell_value != 0:
                if sketch_mode and selected == (i, j):
                    text = sketch_font.render(str(cell_value), True, (128, 128, 128))
                else:
                    text = font.render(str(cell_value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(x + 25, y + 25))
                win.blit(text, text_rect.topleft)

    for i in range(0, 10):
        line_thickness = 4 if i % 3 == 0 else 2
        pygame.draw.line(win, GRID_COLOR, (68 + 50 * i, 67), (68 + 50 * i, 517), line_thickness)
        pygame.draw.line(win, GRID_COLOR, (68, (50 + 50 * i) + 17), (518, (50 + 50 * i) + 17), line_thickness)

def restart_game():
    global selected_difficulty, selected_cell, selected_number, game_over, sudoku
    selected_difficulty = None
    selected_cell = None
    selected_number = None
    game_over = False
    size = 9
    removed = 30
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()

initial_board = None
def reset_game():
    global sudoku, initial_board

    if initial_board and sudoku:
        for i in range(9):
            for j in range(9):
                if not initial_board[i][j]:
                    sudoku.board[i][j] = 0

def draw_buttons(win, buttons):
    button_font = pygame.font.Font(None, 36)

    for button in buttons:
        pygame.draw.rect(win, button.color, button.rect)
        text = button_font.render(button.text, True, FONT_COLOR)
        win.blit(text, button.text_position)

def draw_title(win):
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Welcome to Sudoku", True, FONT_COLOR)
    title_text2 = title_font.render("Select Game Mode", True, FONT_COLOR)
    title_position = ((WIDTH - title_text.get_width()) // 2, 50)
    title_position2 = ((WIDTH - title_text2.get_width()) // 2, title_position[1] + title_text.get_height() + 10)  # Adjusted vertical position

    win.blit(title_text, title_position)
    win.blit(title_text2, title_position2)

def game_won_screen():
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Game Won")

    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

    game_won_text = font.render("Game Won!", True, (0, 0, 0))

    exit_button = pygame.Rect(150, 200, 200, 50)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        screen.blit(game_won_text, (WIDTH // 2 - game_won_text.get_width() // 2, 150))

        pygame.draw.rect(screen, (0, 100, 255), exit_button)
        exit_text = font_small.render("Exit", True, (0, 0, 0))
        screen.blit(exit_text, (exit_button.x + 60, exit_button.y + 15))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if exit_button.collidepoint(mouse_pos):
                    running = False

        pygame.display.update()

    pygame.quit()
def game_over_screen():
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Game Over")

    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

    game_over_text = font.render("Game Over!", True, (0,0,0))

    restart_button = pygame.Rect(150, 200, 200, 50)

    while True:
        screen.fill(BACKGROUND_COLOR)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 150))

        pygame.draw.rect(screen, (0,100,255), restart_button)
        restart_text = font_small.render("Restart", True, (0,0,0))
        screen.blit(restart_text, (restart_button.x + 60, restart_button.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    return True
        restart_game()

        pygame.display.update()

def draw_game_screen(win, board_instance, selected_cell, sketch_mode, selected_number, game_buttons):
    win.fill(BACKGROUND_COLOR)

    if board_instance.is_complete() and board_instance.check_board():
        if board_instance.is_full():
            game_won_screen(win)
        else:
            game_over_screen(win)
    else:
        draw_title(win)
        draw_grid(win, board_instance, selected_cell, sketch_mode, selected_number)
        draw_buttons(win, game_buttons)
def main():

    global selected_difficulty, selected_cell, selected_number, game_over, sudoku, initial_board, board_instance
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Sudoku')
    board_instance = Board(row=9, cols=9, screen=1, difficulty="hard", board=[[0]*9 for _ in range(9)])
    correct_instance= is_correct_instance(board=[[0]*9 for _ in range(9)])


    start_screen_buttons = [
        DifficultyButton("Easy", pygame.Rect(200, 200, 150, 50), (0,100,255), (220, 215)),
        DifficultyButton("Medium", pygame.Rect(200, 300, 150, 50), (0,100,255), (205, 315)),
        DifficultyButton("Hard", pygame.Rect(200, 400, 150, 50), (0,100,255), (225, 415)),
    ]

    game_screen_buttons = [
        GameButton("Reset", pygame.Rect(50, 520, 100, 30), (0,100,255), (70, 525), "reset"),
        GameButton("Restart", pygame.Rect(180, 520, 100, 30), (0,100,255), (185, 525), "restart"),
        GameButton("Exit", pygame.Rect(310, 520, 100, 30), (0,100,255), (330, 525), "exit"),
    ]

    selected_difficulty = None
    selected_cell = None
    selected_number = None
    game_over = False
    initial_board = None

    sketch_mode = False
    sketch_mode_activated = False

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if selected_difficulty and selected_cell is not None:
                    sketch_mode = True
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        selected_number = event.key - pygame.K_0
                        cell_value = sudoku.get_board()[selected_cell[0]][selected_cell[1]]

                        if (sketch_mode or cell_value == 0) and not initial_board[selected_cell[0]][selected_cell[1]]:

                            sudoku.get_board()[selected_cell[0]][selected_cell[1]] = selected_number
                            print(f"Setting cell {selected_cell} to {selected_number} (Sketch mode: {sketch_mode})")
                            print("Current state of the board:")
                            print(sudoku.get_board())
                    elif event.key == pygame.K_RETURN:

                        cell_value = sudoku.get_board()[selected_cell[0]][selected_cell[1]]
                        if sketch_mode and cell_value != 0 and not initial_board[selected_cell[0]][selected_cell[1]]:
                            print(f"Submitting guess for cell {selected_cell}")
                            print("Current state of the board:")
                            print(sudoku.get_board())
                            sketch_mode = False
                    elif event.key == pygame.K_UP and selected_cell[0] > 0:
                        selected_cell = (selected_cell[0] - 1, selected_cell[1])
                    elif event.key == pygame.K_DOWN and selected_cell[0] < 8:
                        selected_cell = (selected_cell[0] + 1, selected_cell[1])
                    elif event.key == pygame.K_LEFT and selected_cell[1] > 0:
                        selected_cell = (selected_cell[0], selected_cell[1] - 1)
                    elif event.key == pygame.K_RIGHT and selected_cell[1] < 8:
                        selected_cell = (selected_cell[0], selected_cell[1] + 1)
                    elif sketch_mode and pygame.K_1 <= event.key <= pygame.K_9:

                        selected_number = event.key - pygame.K_0
                        cell_value = sudoku.get_board()[selected_cell[0]][selected_cell[1]]
                        if not initial_board[selected_cell[0]][selected_cell[1]]:

                            sudoku.get_board()[selected_cell[0]][selected_cell[1]] = selected_number
                            print(f"Setting cell {selected_cell} to {selected_number} (Sketch mode: {sketch_mode})")
                            print("Current state of the board:")
                            print(sudoku.get_board())


                if sketch_mode and sudoku.get_board()[selected_cell[0]][selected_cell[1]] == 0:
                    print(f"Entering sketch mode for cell {selected_cell}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not selected_difficulty:
                    for button in start_screen_buttons:
                        if button.rect.collidepoint(pos):
                            selected_difficulty = button.text
                            size = 9
                            removed = 30
                            if selected_difficulty == "Medium":
                                removed = 40
                            elif selected_difficulty == "Hard":
                                removed = 50
                            sudoku = SudokuGenerator(size, removed)
                            sudoku.fill_values()
                            sudoku.remove_cells()

                            initial_board = [[cell != 0 for cell in row] for row in sudoku.get_board()]
                else:
                    for button in game_screen_buttons:
                        if button.rect.collidepoint(pos):
                            if button.action == "reset":
                                print("Reset clicked")
                                sketch_mode = False
                                reset_game()
                            elif button.action == "restart":
                                selected_difficulty = None
                                selected_cell = None
                                sudoku = None
                                sketch_mode = False
                            elif button.action == "exit":
                                run = False

                if selected_difficulty:
                    selected_cell = ((pos[1] - 50) // 50, (pos[0] - 50) // 50)
                    sketch_mode = True

        if selected_difficulty:
            win.fill(BACKGROUND_COLOR)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                if board_instance.is_full():
                    if sudoku.get_board() == initial_board:
                        game_won_screen()
                    else:
                        game_over_screen()

            else:
                draw_title(win)
                draw_grid(win, sudoku, selected_cell, sketch_mode, selected_number)
                draw_buttons(win, game_screen_buttons)
        else:
            win.fill(BACKGROUND_COLOR)
            draw_title(win)
            draw_buttons(win, start_screen_buttons)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
     main()