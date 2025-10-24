from typing import Iterable
from math import floor, ceil, remainder

class Board:
    rows: list[list[int]]
    size: int

    def __init__(self, size: int):
        self.size = size
        self.rows = [[0 for i in range(size)] for i in range(size)]
    
    def set_board(self, board: list[int]):
        for rownum in range(self.size):
            for colnum in range(self.size):
                self.rows[rownum][colnum] = board[rownum*self.size+colnum]
                
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
                row_char="─"

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

    def get_group_neighbors(self, row:int, col:int):
        row_block=floor(row/3)
        col_block=floor(col/3)
        neighbors = []
        for row_offset in range(3):
            for col_offset in range(3):
                if row_offset == row % 3 and col_offset == col %3:
                    continue

                val = self.rows[row_block*3 + row_offset][col_block*3 + col_offset]
                neighbors.append(val)
        return neighbors

    def get_col_neighbors(self, row:int, col:int):
        col_neighbors = [i[col] for i in self.rows]
        col_neighbors.pop(row)
        return col_neighbors

    def get_row_neighbors(self, row:int, col:int):
        row_neighbors = self.rows[row][:]
        row_neighbors.pop(col)
        return row_neighbors

    def validate_board(self):
        for rownum, row in enumerate(self.rows):
            for colnum, col in enumerate(row):
                if col in self.get_group_neighbors(rownum,colnum) or col in self.get_row_neighbors(rownum,colnum) or col in self.get_col_neighbors(rownum,colnum):
                    print(f"Validation failed for row {rownum}, col {colnum}")
                    return False
        return True