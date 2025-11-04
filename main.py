import random
from board import Board

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
    board.print_board()


    board.solve_board(0, 0)
    board.print_board()

    print(f"Valid:{board.validate_board()}")

if __name__=="__main__":
    main()