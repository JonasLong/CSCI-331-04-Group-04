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
    size = get_boardsize()
    board = Board(size)
    board.print_board()
    board.set_board([random.randint(0,9) for i in range(size**2)])
    board.print_board()

if __name__=="__main__":
    main()