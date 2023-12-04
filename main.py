
from sudoku_generator import SudokuGenerator
import pygame


WIDTH = 550
background_color = (236, 231, 261)



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
    removed = 30
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    print(board)
#JAI
