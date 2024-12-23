import math, random, pygame

class SudokuGenerator:
    # this is the main info needed
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

#this returns the board
    def get_board(self):
        return self.board

# not needed
    def print_board(self):
        pass

#this shows if num is in the row or not
    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True

    def set_cell(self, row, col, value):
        self.board[row][col] = value

    # this shows if num is in the col or not
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    # this shows if num is in the box
    def valid_in_box(self, row_start, col_start, num):

        for r in range(3):
            for k in range(3):
                if num in self.board[row_start+r] and self.board[col_start+k]:
                    return False
        return True

    # this shows if num is in the row, col and box
    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num:
                return False

        for i in range(9):
            if self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True
#this fills the box
    def fill_box(self, row_start, col_start):
        digits = list(range(1, 10))
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = digits.pop()


#this fills the box diagnolly
    def fill_diagonal(self):
        for box in range(0, self.row_length, self.box_length):
            self.fill_box(box, box)


    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)


    def remove_cells(self):
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:
            row = random.randint(0,self.row_length-1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, selected=False):
        cell_size = 50
        font = pygame.font.Font(None, 36)

        x = self.col * cell_size
        y = self.row * cell_size

        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, cell_size, cell_size))

        if selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, cell_size, cell_size), 3)

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 15, y + 15))
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

class is_correct_instance():
    def __init__(self,board):
        self.board= board

    def get_board(self):
        return self.board
    def check_board(self):
        for i in range(len(self.board)):
            if not self.check_row(i) or not self.check_col(i):
                return False
        return True

    def check_row(self, row):
        seen = set()
        for value in self.board[row]:
            if value == 0:
                continue
            if value in seen:
                return False
            seen.add(value)
        return True

    def check_col(self, col):
        seen = set()
        for i in range(len(self.board)):
            value = self.board[i][col]
            if value == 0:
                continue
            if value in seen:
                return False
            seen.add(value)
        return True

    def check_box(board, start_row, start_col):
        seen = set()
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                value = board[i][j]
                if value == 0 or value in seen:
                    return False
                seen.add(value)
        return True


class Board:
    def __init__(self, row, cols, screen, difficulty,board):
        self.row = row
        self.cols = cols
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, i, j, screen) for j in range(row)] for i in range(cols)]
        self.selected_cell = None
        self.board = board
        self.board_rows = len(self.board)
        self.board_cols = len(self.board[0])


    def draw(self):
        cell_size = 50
        for i in range(self.height + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width * cell_size, i * cell_size), 2)
        for j in range(self.width + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (j * cell_size, 0), (j * cell_size, self.height * cell_size), 2)

        for i in range(0, self.height, 3):
            for j in range(0, self.width, 3):
                pygame.draw.rect(self.screen, (0, 0, 0), (j * cell_size, i * cell_size, 3 * cell_size, 3 * cell_size), 3)

        for row in self.cells:
            for cell in row:
                cell.draw(selected=(cell == self.selected_cell))

    def is_complete(self):
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.cells[col][row] == 0:
                    return False
        return True




    def select(self, row, col):
        self.selected_cell = (row, col)

    def click(self, x, y):
        # Calculate the row and column based on coordinates
        row = y // cell_size
        col = x // cell_size

        if 0 <= row < self.size and 0 <= col < self.size:
            return row, col
        else:
            return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = 0

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = value

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = value


    def is_full(self):
        # Check rows
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.cells[col][row]==0:
                    return False
        return True

    def update_board(self):
        pass

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board