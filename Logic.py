import math
import random


def GenerateBoard(difficulty):

    #Initialising reference values
    if difficulty == 'Easy':
        boardSize = 100
    elif difficulty == 'Medium':
        boardSize = 400
    else:
        boardSize = 900
    numBombs = boardSize//10
    print(numBombs)
    dimension = int(math.sqrt(boardSize))


    #Initialising empty board into 3D array
    board = [[[False,0,False] for x in range(dimension)] for y in range(dimension)] #Bomb(T/F), AdjacentBombs, TileIsRevealedToUser


    #Adding bombs to random tiles
    for bomb in range(numBombs):
        freeSpace = False
        while not freeSpace:
            randXPos = random.randint(0,len(board)-1)
            randYPos = random.randint(0,len(board[0])-1)

            if board[randXPos][randYPos][0] == False:
                freeSpace = True
                board[randXPos][randYPos][0] = True


    #Getting number of bombs adjacent to tile for each tile
    for x in range(len(board)):
        for y in range(len(board[0])):
            board[x][y][1] = getNumAdjacentBombs(x,y,board)
           
    return board




def getNumAdjacentBombs(x,y,board):
    numAdjacentBombs = 0
    DIRECTIONS = [
        (-1,-1),
        (-1,0),
        (-1,1),
        (0,-1),
        #(0,0),
        (0,1),
        (1,-1),
        (1,0),
        (1,1)
    ]

    for x_offset, y_offset in DIRECTIONS:
        new_x, new_y = x+x_offset, y+y_offset

        #Checking if new_x and new_y are out of bounds of the board
        if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
            if board[new_x][new_y][0] == True:
                numAdjacentBombs += 1

    return numAdjacentBombs
