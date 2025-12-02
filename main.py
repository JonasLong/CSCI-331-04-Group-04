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
    #bd = [i%10 for i in range(board.size**2)] # testing

    board.set_board(bd)
    print("Starting board:")
    board.print_board()

    #print("Listing board diagonals")
    #for i in range(9):
    #    for j in range(9):
    #        print(f"r={i},c={j},v={board.get_cell(i,j)}")
    #        print(f"n={board.get_diagonal_neighbors(i,j)}")

    print("DFS")
    start = time()
    b1=board.solve_naieve_dfs_no_side_effects(board, 0, 0)
    end = time()
    if b1 is None:
        print("DFS: Board is not solveable")
    else:
        b1.print_board()
        print(f"Solve time: {end-start}s")
        print(f"Valid: {b1.validate_board()}")

    print("DFS with backtracking")
    start = time()
    b2=board.solve_dfs_no_side_effects(board, 0, 0)
    end = time()
    if b2 is None:
        print("DFS backtrack: Board is not solveable")
    else:
        b2.print_board()
        print(f"Solve time: {end-start}s")
        print(f"Valid: {b2.validate_board()}")

    print("DFS with forward checking")
    start = time()
    b3=board.solve_dfs_forward_checking(board, 0, 0)
    end = time()
    if b3 is None:
        print("DFS forward checking: Board is not solveable")
    else:
        b3.print_board()
        print(f"Solve time: {end-start}s")
        print(f"Valid: {b3.validate_board()}")

    #TODO DFS with forward checking and backtracking
    # solve_dfs_forward_checking_and_backtracking(board,0,0)

if __name__=="__main__":
    main()