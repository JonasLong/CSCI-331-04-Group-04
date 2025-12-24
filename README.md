# Customized Sudoku
Final project for CSCI-331-04. Presentation slides are available [here](resources/AI%20project%20presentation.pdf).

## Abstract
This project generates a random sudoku board and solves it, using both a naive Depth-First-Search algorithm and a more advanced search that uses Constraint Satisfaction Problem solving strategies to prune invalid states with forward checking

## Developers
Jonas Long:
Board/cell classes, grid randomization, col/row/group neighbors, board validation, naive algorithm, backtracking, and presentation

Justin Guidry:
Made simple backtracking with set board, implemented forward checking, optimizations, and presentation

## How to run the project
From the project directory, run `python code/main.py`
The board will be initalized using the csv board state in `data/board.txt`
