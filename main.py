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

    ran = [random.randint(0,9) for i in range(size**2)]
    #ran = [i%10 for i in range(size**2)] # testing

    board.set_board(ran)
    board.print_board()

    row = int(input("Enter row >"))
    col = int(input("Enter col >"))

    print(board.get_group_neighbors(row,col))
    print(board.get_row_neighbors(row,col))
    print(board.get_col_neighbors(row,col))

    print(f"Valid:{board.validate_board()}")

if __name__=="__main__":
    main()