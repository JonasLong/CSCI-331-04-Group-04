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

def load_board():
    with open("data/board.txt") as b:
        bd= "".join(b.readlines()).replace(" ","").split(",")
        return [int(cell) for cell in bd]

def main():
    
    board = Board(9)

    board2 = Board(9)

    bd = load_board() 
    

    board.set_board(bd)
    board.set_domains()

    board2.set_board(bd)
    board2.set_domains()
    print("Starting board:")
    board.print_board()


    print("DFS")
    start = time()
    board.solve_naive( 0, 0, board.domains)
    end = time()
    board.print_board()
    print(f"Solve time: {end-start}s")
    print(f"Total branches explored: {board.branches}")

    print("DFS with forward checking")
    start = time()
    board2.solve_dfs( 0, 0, board2.domains)
    end = time()
    board2.print_board()
    print(f"Solve time: {end-start}s")
    print(f"Total branches explored: {board2.branches}")

if __name__=="__main__":
    main()