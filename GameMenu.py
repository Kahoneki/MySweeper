import pygame
from Logic import *
from HighScoreLogic import *

#----PYGAME INITIALISATION AND VARIABLES----#

pygame.font.init()

TILE_SRC = pygame.image.load('Media/Tile.png')
BOMB = pygame.image.load('Media/bomb.png')
STOPWATCH = pygame.image.load('Media/stopwatch.png')
FLAG_NO_BORDER = pygame.transform.scale(pygame.image.load(f'Media/flagNoBackground.png'),(40,40))
BACK = pygame.image.load('Media/back.png')

SMALL_FONT = pygame.font.SysFont('Comic Sans MS',28)
LARGE_FONT = pygame.font.SysFont('Comic Sans MS', 128)
GAME_OVER = LARGE_FONT.render('GAME OVER', True, (255,0,0))
WIN_TEXT = LARGE_FONT.render('YOU WIN!', True, (0,255,0))
NEWHIGHSCORE_TEXT = LARGE_FONT.render('NEW HIGH SCORE!', True, (0,0,255))

BISQUE = (242,210,189)
DARKBISQUE = (242,174,128)

#----END OF PYGAME INITIALISATION AND VARIABLES----#


#Used for resizing sprites based on the selected difficulty.
def resizeTile(tilesrc):
    return pygame.transform.scale(tilesrc,(660/len(board),660/len(board[0])))

def GameMenu(_win,_fps,difficulty,_username):

    #2D array that stores all the objects that have to be drawn to the screen in the format [xPosition, yPosition, object]
    global objectsToDraw
    objectsToDraw = []
    
    global WIN
    WIN = _win

    global FPS
    FPS = _fps
    
    global seconds
    seconds = 0
    global FRAMECOUNT #Used for stopwatch
    FRAMECOUNT = 0

    global backButton
    backButton = pygame.Rect(50,50,50,50)

    global USERNAME
    USERNAME = _username
    global board
    board = GenerateBoard(difficulty)
    
    global FLAG
    FLAG = resizeTile(pygame.image.load(f'Media/flag.png'))
    global numFlags
    numFlags = 0

    global TILE
    TILE = resizeTile(TILE_SRC)

    #Used to ensure the user's first click isn't a bomb
    firstClick = True

    clock = pygame.time.Clock()

    lose = False
    win = False
    gameOver = False
    while not lose and not win:
        clock.tick(FPS)
        FRAMECOUNT += 1
        seconds = int(FRAMECOUNT/FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = True
                return False,0

            if event.type == pygame.MOUSEBUTTONDOWN and gameOver == False:
                if backButton.collidepoint(event.pos):
                    return True,0
                mousePosX = pygame.mouse.get_pos()[0]
                mousePosY = pygame.mouse.get_pos()[1]
                if 190 <= mousePosX <= 850 and 80 <= mousePosY <= 740: #Inside board boundaries
                    tileXIndex = int((mousePosX-startXPos)/tileSize)
                    tileYIndex = int((mousePosY-startYPos)/tileSize)
                    
                    if event.button == 1: #Left click
                        if firstClick:
                            board = makeFirstClick0Tile(tileXIndex,tileYIndex,difficulty)
                        else:
                            if board[tileXIndex][tileYIndex][0] == True:
                                gameOver = True
                                lose = True
                        firstClick = False
                        Click(tileXIndex,tileYIndex,"left",objectsToDraw)
                        
                    elif event.button == 3: #Right click                        
                        numFlags += Click(tileXIndex,tileYIndex,"right",objectsToDraw)
        
        #Cheat code - For testing purposes
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            win = True
            gameOver = True

        
        draw_board(seconds)
        
        #Player wins if all non-bomb tiles are revealed
        notRevealedTiles = 0
        for row in board:
            for tile in row:
                if tile[2] == False:
                    notRevealedTiles += 1
        if notRevealedTiles == (len(board)*len(board))//10: #Same as numBombs in Logic.py (10/40/90)
            win = True
        
    if lose:
        objectsToDraw.append([150,300,GAME_OVER])
    
    else:
        objectsToDraw.append([150,300,WIN_TEXT])
        if USERNAME:
            if CheckNewHighScore(USERNAME,difficulty,seconds):
                objectsToDraw.append([150,500,NEWHIGHSCORE_TEXT])
                UpdateUserHighScore(USERNAME,difficulty,seconds)
    draw_board(seconds)
    pygame.time.wait(1000)
    return True,0




#Ensures that the first click will be a blank tile (not a bomb and no adjacent bombs), meaning that the first click will always start a flood fill
def makeFirstClick0Tile(tileXIndex,tileYIndex,difficulty):
    newBoard = board
    #Keep generating new boards until requirement is met
    while newBoard[tileXIndex][tileYIndex][0] == True or newBoard[tileXIndex][tileYIndex][1] != 0:
        newBoard = GenerateBoard(difficulty)
    return newBoard




def Click(tileXIndex, tileYIndex, button, objectsToDraw):
    sprXPos = startXPos+(tileXIndex*tileSize)
    sprYPos = startYPos+(tileYIndex*tileSize)


    #Left click
    if button == "left":
        #Stop objects being drawn to screen multiple times from multiple clicks of the same tile
        for obj in objectsToDraw:
            if sprXPos == obj[0] and sprYPos == obj[1]:
                return

        #Bomb tile
        if board[tileXIndex][tileYIndex][0] == True:
            objectsToDraw.append([sprXPos,sprYPos,resizeTile(BOMB)])

        #Blank tile
        elif board[tileXIndex][tileYIndex][1] == 0:
            ClearTiles(tileXIndex,tileYIndex)
                
        #Numbered tile
        elif board[tileXIndex][tileYIndex][1] != 0:
            UNSCALED_TILE = pygame.image.load(f'Media/{board[tileXIndex][tileYIndex][1]}.png')
            objectsToDraw.append([sprXPos,sprYPos,resizeTile(UNSCALED_TILE)])

        board[tileXIndex][tileYIndex][2] = True #Mark tile as revealed


    #Right click
    else:
        #Remove flag if there's already one on the tile and decrease numFlags by 1
        for obj in objectsToDraw:
            if sprXPos == obj[0] and sprYPos == obj[1] and board[tileXIndex][tileYIndex][2] == False:
                objectsToDraw.remove(obj)
                return -1

        #Add flag and increment numFlags by 1
        #Checking if user has flags left - (len(board)*len(board))//10 is the number of bombs (10/40/90)
        if numFlags < (len(board)*len(board))//10:
            if board[tileXIndex][tileYIndex][2] == False: #Checking if tile hasn't already been revealed to user
                objectsToDraw.append([sprXPos,sprYPos,FLAG])
                return 1
            else:
                return 0
        else:
            return 0



#Flood fill algorithm
def ClearTiles(x,y):
    # draw_board(seconds)
    #Border check
    if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
        return
    
    #Flood has hit revealed tile check
    if board[x][y][2] == True:
        return


    sprXPos = startXPos+(x*tileSize)
    sprYPos = startYPos+(y*tileSize)
    #Edge of fill check + drawing numbered tiles
    if board[x][y][1] != 0:
        UNSCALED_TILE = pygame.image.load(f'Media/{board[x][y][1]}.png')
        objectsToDraw.append([sprXPos,sprYPos,resizeTile(UNSCALED_TILE)])
        board[x][y][2] = True
        return
    
    #Drawing empty tiles
    UNSCALED_TILE = pygame.image.load(f'Media/0.png')
    objectsToDraw.append([sprXPos,sprYPos,resizeTile(UNSCALED_TILE)])
    board[x][y][2] = True

    ClearTiles(x-1,y)
    ClearTiles(x+1,y)
    ClearTiles(x,y-1)
    ClearTiles(x,y+1)




def draw_board(seconds):
    WIN.fill(BISQUE)
    
    #Drawing initial tiles to screen
    global startXPos
    global startYPos
    global tileSize
    startXPos = 190
    startYPos = 80
    tileSize = 660/len(board)
    for i in range(len(board)):
        for k in range(len(board[0])):
            WIN.blit(TILE,(startXPos+(i*tileSize), startYPos+(k*tileSize)))

    for obj in objectsToDraw:
        WIN.blit(obj[2],(obj[0],obj[1]))

    WIN.blit(FLAG_NO_BORDER,(600,24))
    WIN.blit(SMALL_FONT.render(str(numFlags),True,(0,0,0)),(640,24))
    
    WIN.blit(STOPWATCH, (300,30))
    minutes,seconds = divmod(seconds,60)
    if seconds < 10:
        seconds = f"0{seconds}" #So that small second values will be displayed as 1:02 instead of 1:2
    WIN.blit(SMALL_FONT.render(f"{minutes}:{seconds}",True,(0,0,0)), (340,25))

    if USERNAME:
        WIN.blit(SMALL_FONT.render(USERNAME,True,(0,0,0)),(30,695))


    pygame.draw.rect(WIN,DARKBISQUE,backButton)
    WIN.blit(BACK,(backButton.x,backButton.y))

    pygame.display.update()
