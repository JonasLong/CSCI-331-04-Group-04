from typing import Iterable


class Board:
    rows: list[list[int]]
    size: int

    def __init__(self, size: int):
        self.size = size
        self.rows = [[0 for i in range(size)] for i in range(size)]
    
    def set_board(self, iter):
        for rownum in range(self.size):
            for colnum in range(self.size):
                self.rows[rownum][colnum] = iter[rownum+colnum]
                

    def get_cell(self, row: int, col: int):
        return self.rows[row][col]

    def print_board(self):
        self._get_row_sep(-1)
        for rownum, row in enumerate(self.rows):
            self._get_col_sep(rownum, -1)
            for colnum, col in enumerate(row):
                print(col, end="")
                self._get_col_sep(rownum, colnum)
            self._get_row_sep(rownum)
        print()

    def _get_row_sep(self, row:int):
        print()
        print(" ",end="")
        col_intercept=""
        for col in range(self.size):
            if (row+1) % 3 == 0:
                row_char="═"
            else:
                row_char="-"

            if (col) % 3 == 0:
                if (row+1) % 3 == 0:
                    col_intercept="╬"
                else:
                    col_intercept="║"

                rowitem = col_intercept + row_char*3
            else:
                rowitem = row_char*4

            print(rowitem, end="")
        print(col_intercept)
        

    def _get_col_sep(self, row:int, col:int):

        if (col+1)%3 == 0:
            print(" ║ ",end="")
        else:
            print(" | ",end="")