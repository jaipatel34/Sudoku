import math, random


class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))



    def get_board(self):
        return self.board


    def print_board(self):
        pass


    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True


    def valid_in_col(self, col, num):

        if num in self.board[col]:
            return False
        else:
            return True


    def valid_in_box(self, row_start, col_start, num):

        for r in range(3):
            for k in range(3):
                if num in self.board[row_start+r] and self.board[col_start+k]:
                    return False
        return True


    def is_valid(self, row, col, num):
        if num in self.board[col]:
            return False
        elif num in self.board[row]:
            return False
        for i in range(3):
            for j in range(3):
                if (num in self.board[row+i]) or (num in self.board[col+j]):
                    return False
        return True


    def fill_box(self, row_start, col_start):
        digits = list(range(1, 10))
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = digits.pop()



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
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board



#abcdefg