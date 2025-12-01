import random
from board import Board
from time import time

def get_boardsize():
    while True:
        size=input("Enter size (default 9, must be a mult of 3)\n>")
        if size=="":
            size=9
        else:
            size=int(size)

        if size % 3 == 0:
            return size

def main():
    #size = get_boardsize()
    board = Board(9)

    bd = [ 0, 0, 9, 0, 4, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 5, 3, 1, 0,
           0, 6, 1, 0, 0, 8, 0, 5, 0,
           0, 0, 5, 4, 0, 0, 2, 0, 3,
           0, 1, 0, 0, 0, 7, 0, 0, 8,
           0, 8, 0, 0, 0, 0, 7, 6, 0,
           3, 0, 6, 0, 1, 9, 4, 0, 0,
           7, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 4, 0, 5, 0, 6, 2, 7 ]
    #ran = [i%10 for i in range(size**2)] # testing

    board.set_board(bd)
    print("Starting board:")
    board.print_board()

    print("DFS")
    start = time()
    b1=board.solve_naieve_dfs_no_side_effects(board, 0, 0)
    end = time()
    assert(b1 is not None)
    b1.print_board()
    print(f"Solve time: {end-start}s")
    print(f"Valid: {b1.validate_board()}")

    print("DFS with backtracking")
    start = time()
    b2=board.solve_dfs_no_side_effects(board, 0, 0)
    end = time()
    assert(b2 is not None)
    b2.print_board()
    print(f"Solve time: {end-start}s")
    print(f"Valid: {b2.validate_board()}")

if __name__=="__main__":
    main()