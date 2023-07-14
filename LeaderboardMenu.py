import pygame
from DBFunctions import *
from HighScoreLogic import *


#----PYGAME INITIALISATION AND VARIABLES----#

pygame.font.init()

SMALL_FONT = pygame.font.SysFont('Comic Sans MS', 28)
FONT = pygame.font.SysFont('Comic Sans MS',64)

BIN = pygame.image.load('Media/bin.png')
BACK = pygame.image.load('Media/back.png')

BISQUE = (242,210,189)
DARKBISQUE = (242,174,128)
DARKERBISQUE = (242,134,88)

#----END OF PYGAME INITIALISATION AND VARIABLES----#


def LeaderboardMenu(_win,FPS,_username):
    global WIN
    WIN = _win
    global USERNAME
    USERNAME = _username

    selectedDifficulty = 'Easy'

    #Used to refresh the leaderboard when user changes difficulty or when admin deletes a high score
    refreshLeaderboard = True
    
    global sortedHighScores

    global easyButton
    easyButton = pygame.Rect(425,50,150,50)
    global mediumButton
    mediumButton = pygame.Rect(600,50,150,50)
    global expertButton
    expertButton = pygame.Rect(775,50,150,50)
    
    global leaderboardBackground
    leaderboardBackground = pygame.Rect(50,150,875,550)

    global highScoreRects
    highScoreRects = []
    
    global deleteIcons
    deleteIcons = []

    for i in range(5):
        highScoreRects.append(pygame.Rect(75,(175+105*i),825,80))
        deleteIcons.append(pygame.Rect(935,(185+105*i),50,50))

    global backButton
    backButton = pygame.Rect(50,50,50,50)

    clock = pygame.time.Clock()


    while True:
        clock.tick(FPS)

        #To stop the database from being read every frame
        if refreshLeaderboard:
            sortedHighScores = GetSortedHighScores(selectedDifficulty)
            refreshLeaderboard = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False,0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.collidepoint(event.pos):
                    return True,0


                #Changing difficulty
                if easyButton.collidepoint(event.pos) and selectedDifficulty != 'Easy':
                    selectedDifficulty = 'Easy'
                    refreshLeaderboard = True

                if mediumButton.collidepoint(event.pos) and selectedDifficulty != 'Medium':
                    selectedDifficulty = 'Medium'
                    refreshLeaderboard = True

                if expertButton.collidepoint(event.pos) and selectedDifficulty != 'Expert':
                    selectedDifficulty = 'Expert'
                    refreshLeaderboard = True
                
                for i,deleteIcon in enumerate(deleteIcons):
                    if deleteIcon.collidepoint(event.pos):
                        DeleteUserHighScore(sortedHighScores[i][1],selectedDifficulty)
                        refreshLeaderboard = True


        draw_board()







def GetSortedHighScores(selectedDifficulty):
    rows = LoadUsers("leaderboard")

    #List of all high scores of selected difficulty
    sortedHighScores = []
    for row in rows:
        if row[3] == selectedDifficulty:
            sortedHighScores.append(row)
    
    #Insertion sort to sort times from lowest to highest
    for i in range(1,len(sortedHighScores)):
        currentVal = sortedHighScores[i]
        position = i
        while position > 0 and sortedHighScores[position-1][2] > currentVal[2]:
            sortedHighScores[position] = sortedHighScores[position-1]
            position -= 1

        sortedHighScores[position] = currentVal
    
    return sortedHighScores




def draw_board():
    WIN.fill(BISQUE)
    pygame.draw.rect(WIN,DARKBISQUE,easyButton)
    WIN.blit(SMALL_FONT.render("EASY",True,(0,0,0)),(460,55))
    pygame.draw.rect(WIN,DARKBISQUE,mediumButton)
    WIN.blit(SMALL_FONT.render("MEDIUM",True,(0,0,0)),(610,55))
    pygame.draw.rect(WIN,DARKBISQUE,expertButton)
    WIN.blit(SMALL_FONT.render("EXPERT",True,(0,0,0)),(795,55))

    pygame.draw.rect(WIN,DARKBISQUE,leaderboardBackground)
    for hsRect in highScoreRects:
        pygame.draw.rect(WIN,DARKERBISQUE,hsRect)
    for i in range(4):
        WIN.blit(FONT.render(f"{i+1}.",True,(0,0,0)),(85,(170+105*i)))


    userRank = None #Assume the user doesn't have a score
    if USERNAME:
        #Check if user does have a score
        for i,score in enumerate(sortedHighScores):
            if score[1] == USERNAME:
                if i > 4: #userRank doesn't need to be assigned a value if the player is in the top 5, since userRank=None will cause the program to draw the top 5 scores anyway.
                    userRank = i+1
        if userRank:
            WIN.blit(FONT.render(f"{userRank}.",True,(0,0,0)),(85,590))
        else:
            WIN.blit(FONT.render("5.",True,(0,0,0)),(85,590))

    else:
        WIN.blit(FONT.render("5.",True,(0,0,0)),(85,590))



    for i,user in enumerate(sortedHighScores):
        if i <= 4: #In case there are less than 5 scores

            if i == 4 and userRank:
                #Username
                textWidth,textHeight = FONT.size(sortedHighScores[userRank-1][1])[0]
                if textWidth < 670:
                    WIN.blit(FONT.render(sortedHighScores[userRank-1][1],True,(0,0,0)),(140,(170+105*i)))
                else:
                    WIN.blit(SMALL_FONT.render(sortedHighScores[userRank-1][1],True,(0,0,0)),(140,(195+105*i)))
                minutes,seconds = divmod(sortedHighScores[userRank-1][2],60)

                #Time
                if seconds < 10:
                    seconds = f"0{seconds}"
                WIN.blit(FONT.render(f"{minutes}:{seconds}",True,(0,0,0)),(760,(170+105*i)))

            else:
                #Username
                textWidth = FONT.size(user[1])[0]
                if textWidth < 670:
                    WIN.blit(FONT.render(user[1],True,(0,0,0)),(140,(170+105*i)))
                else:
                    WIN.blit(SMALL_FONT.render(user[1],True,(0,0,0)),(140,(195+105*i)))

                #Time
                minutes,seconds = divmod(user[2],60)
                if seconds < 10:
                    seconds = f"0{seconds}"
                WIN.blit(FONT.render(f"{minutes}:{seconds}",True,(0,0,0)),(760,(170+105*i)))
    

    if USERNAME:
        if AdminCheck(USERNAME):
            for i,deleteIcon in enumerate(deleteIcons):
                if i <= len(sortedHighScores)-1:
                    pygame.draw.rect(WIN,DARKBISQUE,deleteIcon)
                    WIN.blit(BIN,(deleteIcon.x,deleteIcon.y))


    pygame.draw.rect(WIN,DARKBISQUE,backButton)
    WIN.blit(BACK,(backButton.x,backButton.y))
    pygame.display.update()
