# Author: Javi Barranco
# Name: 9x9 Sudoku Solver

# The first board the program will solve.
Board1 = [[0,0,0,2,6,0,7,0,1],
          [6,8,0,0,7,0,0,9,0],
          [1,9,0,0,0,4,5,0,0],
          [8,2,0,1,0,0,0,4,0],
          [0,0,4,6,0,2,9,0,0],
          [0,5,0,0,0,3,0,2,8],
          [0,0,9,3,0,0,0,7,4],
          [0,4,0,0,5,0,0,3,6],
          [7,0,3,0,1,8,0,0,0]]

Empty_board = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]


def board_print(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(0,9):
            if j % 3 == 0 and j != 0:
                print(" | ", end = '')
            if j == 8:
                print("{}".format(board[i][j]))
            else:
                print("{} ".format(board[i][j]), end = '')

def valid(board, value, row, col):
    # Check row:
    for i in range(0,9):
        if board[row][i] == value and i != col:
            return False
    # Check col:
    for i in range(0,9):
        if board[i][col] == value and i != row:
            return False
    # Calculate origin of sub-grid:
    grid_r = int(row/3)*3
    grid_c = int(col/3)*3
    # Check sub-grid:
    for i in range(0,3):
        for j in range(0,3):
            if board[grid_r+i][grid_c+j] == value and grid_r+i != row and grid_c+j != col:
                return False
    return True

def locate_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i,j)
    return (-1,-1)

def solve(board):
    pos = locate_empty(board)
    if pos == (-1,-1):
        return True
    else:
        row, col = pos

    for i in range(1,10):
        if valid(board, i, row, col) == True:
            board[row][col] = i

            if solve(board) == True:
                return True
            board[row][col] = 0
    return False
