from typing import Iterable
from math import floor, ceil, remainder
from typing import Self

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

    def copy_board(self, board: Self):
        self.rows = [i[:] for i in board.rows]
                
    def get_cell(self, row: int, col: int):
        return self.rows[row][col]
    
    def set_cell(self, row:int, col:int, val:int):
        self.rows[row][col] = val

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
    
    def is_safe_move(self, row:int, col:int, val:int):
        rowneb = self.get_row_neighbors(row, col)
        colneb = self.get_col_neighbors(row, col)
        groupneb = self.get_group_neighbors(row, col)

        if val in rowneb or val in colneb or val in groupneb:
            return False
        return True

    @classmethod
    def solve_naieve_dfs_no_side_effects(cls, board, row:int, col:int) -> Self | None:
        if row == 8 and col == 9:
            return board
        if col == 9:
            row += 1
            col = 0
        if board.get_cell(row, col) > 0:
            return cls.solve_dfs_no_side_effects(board, row, col + 1)
        for val in range (1, 10):
            new_board = Board(board.size)
            #board.print_board()
            new_board.copy_board(board)
            #new_board.print_board()
            new_board.set_cell(row, col, val)
            res = cls.solve_dfs_no_side_effects(new_board, row, col + 1)
            if res is not None:
                return res
        return None

    def solve_dfs(self, row:int, col:int) -> bool:
        if row == 8 and col == 9:
            return True
        if col == 9:
            row += 1
            col = 0
        if self.get_cell(row, col) > 0:
            return self.solve_dfs(row, col + 1)
        for val in range (1, 10):
            if self.is_safe_move(row, col, val):
                self.set_cell(row, col, val)
                if self.solve_dfs(row, col + 1):
                    return True
            self.set_cell(row, col, 0)
        return False

    @classmethod
    def solve_dfs_no_side_effects(cls, board, row:int, col:int) -> Self | None:
        if row == 8 and col == 9:
            return board
        if col == 9:
            row += 1
            col = 0
        if board.get_cell(row, col) > 0:
            return board.solve_dfs_no_side_effects(board, row, col + 1)
        for val in range (1, 10):
            if board.is_safe_move(row, col, val):
                new_board = Board(board.size)
                new_board.copy_board(board)
                new_board.set_cell(row, col, val)
                res = cls.solve_dfs_no_side_effects(new_board, row, col + 1)
                if res is not None:
                    return res
        return None
