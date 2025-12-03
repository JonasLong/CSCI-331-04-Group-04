import math
from typing import Iterable
from math import floor, ceil, remainder
from typing import Self

# Consider diagonals when validating the board
USE_DIAGONALS = True
# If set, cells can only have diagonal neighbors when they're on the board's diagonals
# If not set, every cell can have diagonal neighbors extending up and down the board
ONLY_PURE_DIAGONALS = True

class Board:
    rows: list[list[int]]
    size: int
    domains: list[list[int]]
    branches: int

    def __init__(self, size: int):
        self.size = size
        self.rows = [[0 for i in range(size)] for i in range(size)]
        self.domains = [[] for s in range(size*size)]
        self.branches = 0
    
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
            if not (row==col or row==self.size-col-1):
                return []
            
        ogrow = row
        if row == col and not (row==self.size-col-1):
            row = 0
            col = 0
        if not (row == col) and row==self.size-col-1:
            row = 0
            col = 8


        # left and right diagonals are the vertical halves of the X formed on the target cell
        diag_left=[]
        diag_right=[]
        for (rowind, rowlst) in enumerate(self.rows):
            if rowind == ogrow:
                # Don't include self in neighbor list
                continue

            if rowind == 0:
                if col == 0:
                    diag_left.append(rowlst[0])
                    continue
                if col == 8:
                    diag_left.append(rowlst[8])
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
    def solve_naive_dfs_no_side_effects(cls, board, row:int, col:int) -> Self | None:
        if row == 8 and col == 9:
            if board.validate_board():
                return board
            else:
                return None
        if col == 9:
            row += 1
            col = 0
        if board.get_cell(row, col) > 0:
            return cls.solve_naive_dfs_no_side_effects(board, row, col + 1)
        for val in range (1, 10):
            new_board = Board(board.size)
            #board.print_board()
            new_board.copy_board(board)
            #new_board.print_board()
            new_board.set_cell(row, col, val)
            res = cls.solve_naive_dfs_no_side_effects(new_board, row, col + 1)
        return None

    def solve_dfs(self, row:int, col:int, domains) -> bool:
        if row == 8 and col == 9:
            return True
        if col == 9:
            row += 1
            col = 0
        if self.get_cell(row, col) > 0:
            new_domain = self.update_domains(row, col, self.get_cell(row, col), domains)
            if not new_domain:
                return False
            return self.solve_dfs(row, col + 1, new_domain)
        for val in domains[row*self.size + col]:
            if self.is_safe_move(row, col, val):
                new_domain = self.update_domains(row, col, val, domains)
                if new_domain:
                    self.set_cell(row, col, val)
                    self.branches += 1
                    if self.solve_dfs(row, col + 1, new_domain):
                        return True
            self.set_cell(row, col, 0)
        return False
    
    def solve_naive(self, row, col, domains):
        if row == 8 and col == 9:
            if self.validate_board():
                return True
            else:
                return False
        if col == 9:
            row += 1
            col = 0
        if self.get_cell(row, col) > 0:
            new_domains = [i[:] for i in domains]
            return self.solve_naive(row, col + 1, new_domains)
        for i in range(1,10):
            if self.is_safe_move(row, col, i):
                self.branches += 1
                self.set_cell(row, col, i)
                new_domains = [i[:] for i in domains]
                if self.solve_naive(row, col + 1, new_domains):
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
    
    def set_domains(self):
        for rownum, row in enumerate(self.rows):
            for colnum, col in enumerate(row):
                if col > 0:
                    self.domains[rownum*self.size + colnum] = [col]
                else:
                    self.domains[rownum*self.size + colnum] = [i for i in range(1,10)]

    
    def update_domains(self, row:int, col:int, val:int, domains):
        new_domains = [i[:] for i in domains]
        for i in self.get_col_domneighbors(row, col):
            if val in new_domains[i]:
                new_domains[i].remove(val)
            if not new_domains[i]:
                return []
        for i in self.get_row_domneighbors(row, col):
            if val in new_domains[i]:
                new_domains[i].remove(val)
            if not new_domains[i]:
                return []
        for i in self.get_group_domneighbors(row, col):
            if val in new_domains[i]:
                new_domains[i].remove(val)
            if not new_domains[i]:
                return []
        for i in self.get_diagonal_domneighbors(row, col):
            if val in new_domains[i]:
                new_domains[i].remove(val)
            if not new_domains[i]:
                return []
        return new_domains
    

    def get_group_domneighbors(self, row:int, col:int):
        row_block=floor(row/3)
        col_block=floor(col/3)
        neighbors = []
        for row_offset in range(3):
            for col_offset in range(3):
                if row_offset == row % 3 and col_offset == col %3:
                    continue

                val = (row_block*3 + row_offset)*self.size + (col_block*3 + col_offset)
                neighbors.append(val)
        return neighbors

    def get_col_domneighbors(self, row:int, col:int):
        col_neighbors = [(i*self.size + col) for i in range(0,9)]
        col_neighbors.pop(row)
        return col_neighbors

    def get_row_domneighbors(self, row:int, col:int):
        row_neighbors = []
        domain_start = row*self.size
        for i in range(0,9):
            row_neighbors.append(i+domain_start)
        row_neighbors.pop(col)
        return row_neighbors

    def get_diagonal_domneighbors(self, row:int, col:int):
        # If only_pure is set, cells can only have diagonal neighbors when they're on the board's diagonals
        # If not set, every cell can have diagonal neighbors extending up and down the board
        if ONLY_PURE_DIAGONALS:
            if not (row==col or row==self.size-col-1):
                return []
            
        ogrow = row
        if row == col and not (row==self.size-col-1):
            row = 0
            col = 0
        if not (row == col) and row==self.size-col-1:
            row = 0
            col = 8


        # left and right diagonals are the vertical halves of the X formed on the target cell
        diag_left=[]
        diag_right=[]
        for (rowind, rowlst) in enumerate(self.rows):
            if rowind == ogrow:
                # Don't include self in neighbor list
                continue

            if rowind == 0:
                if col == 0:
                    diag_left.append(0)
                    continue
                if col == 8:
                    diag_left.append(8)
                    continue

            offset = abs(rowind-row)
            ldiag_col = col-offset
            rdiag_col = col+offset
            #print(f"diags={ldiag_col} & {rdiag_col} on c{rowind}")
            if 0 <= ldiag_col and ldiag_col < self.size:
                diag_left.append(rowind*self.size + ldiag_col)
            if 0 <= rdiag_col and rdiag_col < self.size:
                diag_right.append(rowind*self.size + rdiag_col)
        diag_left.extend(diag_right)
        return diag_left


