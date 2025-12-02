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
    
    board = Board(9)

    board2 = Board(9)

    bd = [ 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 7, 0, 9, 0, 0, 0,
           0, 0, 6, 0, 3, 0, 9, 0, 0,
           0, 6, 0, 2, 7, 5, 0, 1, 0,
           0, 0, 5, 9, 0, 6, 3, 0, 0,
           0, 1, 0, 3, 4, 8, 0, 9, 0,
           0, 0, 7, 0, 8, 0, 5, 0, 0,
           0, 0, 0, 4, 0, 7, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    

    board.set_board(bd)
    board.set_domains()

    board2.set_board(bd)
    board2.set_domains()
    print("Starting board:")
    board.print_board()


    print("DFS")
    start = time()
    board.solve_naieve( 0, 0, board.domains)
    end = time()
    board.print_board()
    print(f"Solve time: {end-start}s")
    print(f"Total brances explored: {board.branches}")

    print("DFS with forward checking")
    start = time()
    board2.solve_dfs( 0, 0, board2.domains)
    end = time()
    board2.print_board()
    print(f"Solve time: {end-start}s")
    print(f"Total brances explored: {board2.branches}")

if __name__=="__main__":
    main()