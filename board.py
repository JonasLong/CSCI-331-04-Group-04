import math
from typing import Iterable
from math import floor, ceil, remainder
from typing import Self

# Consider diagonals when validating the board
USE_DIAGONALS = False
# If set, cells can only have diagonal neighbors when they're on the board's diagonals
# If not set, every cell can have diagonal neighbors extending up and down the board
ONLY_PURE_DIAGONALS = True

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

    def get_diagonal_neighbors(self, row:int, col:int):
        # If only_pure is set, cells can only have diagonal neighbors when they're on the board's diagonals
        # If not set, every cell can have diagonal neighbors extending up and down the board
        if ONLY_PURE_DIAGONALS:
            if not (row==col or row==self.size-col):
                return []

        # left and right diagonals are the vertical halves of the X formed on the target cell
        diag_left=[]
        diag_right=[]
        for (rowind, rowlst) in enumerate(self.rows):
            if rowind == row:
                # Don't include self in neighbor list
                continue

            offset = abs(rowind-row)
            ldiag_col = col-offset
            rdiag_col = col+offset
            #print(f"diags={ldiag_col} & {rdiag_col} on c{rowind}")
            if 0 <= ldiag_col and ldiag_col < self.size:
                diag_left.append(rowlst[ldiag_col])
            if 0 <= rdiag_col and rdiag_col < self.size:
                diag_right.append(rowlst[rdiag_col])
        diag_left.extend(diag_right)
        return diag_left


    def validate_board(self):
        for rownum, row in enumerate(self.rows):
            for colnum, val in enumerate(row):
                if (val in self.get_group_neighbors(rownum,colnum) or 
                    val in self.get_row_neighbors(rownum,colnum) or 
                    val in self.get_col_neighbors(rownum,colnum) or 
                    (USE_DIAGONALS and val in self.get_diagonal_neighbors(rownum,colnum))):
                    print(f"Validation failed for row {rownum}, col {colnum}")
                    return False
        return True
    
    def is_safe_move(self, row:int, col:int, val:int):
        rowneb = self.get_row_neighbors(row, col)
        colneb = self.get_col_neighbors(row, col)
        groupneb = self.get_group_neighbors(row, col)
        diagneb = self.get_diagonal_neighbors(row, col)

        if (val in rowneb or 
        val in colneb or 
        val in groupneb or 
        (USE_DIAGONALS and val in diagneb)):
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

    @classmethod
    def solve_dfs_forward_checking(cls, board, row:int, col:int) -> Self | None:
        # Make a 3D list for row, column, and domain, where domain is numbers 1-9
        domains = [[list(range(1,10)) for i in range(board.size)] for i in range(board.size)]
        print("pre-filled domain list:", domains)

        # replace the domain of cells that are already filled with an empty list
        for rowind, rowval in enumerate(board.rows):
            for colind, val in enumerate(rowval):
                if val > 0:
                    # pre-filled cells have no domain
                    domains[rowind][colind]=[]
        print("\nupdated domains:", domains)

        #TODO:
        #given the list of domains, run a backtracking solver. Returns a valid solution board, or None if not found
        

        pass


    @classmethod
    def solve_dfs_forward_checking_and_backtracking(cls, board, row:int, col:int) -> Self | None:
        # Like the above function, but include the is_safe_move() backtracking
        pass

