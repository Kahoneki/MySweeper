import pygame


#----PYGAME INITIALISATION AND VARIABLES----#

pygame.font.init()

USERNAME_FONT = pygame.font.SysFont('Comic Sans MS', 28)
FONT = pygame.font.SysFont('Comic Sans MS',64)

LOGO = pygame.transform.scale(pygame.image.load('Media/Logo.png'),(770,250))
BISQUE = (242,210,189)
DARKBISQUE = (242,174,128)

BACK = pygame.image.load('Media/back.png')

#----END OF PYGAME INITIALISATION AND VARIABLES----#


def MainMenu(_win,FPS,_username):

    global WIN
    WIN = _win
    global USERNAME
    USERNAME = _username

    #Menu change buttons
    global playSignedInRect
    playSignedInRect = pygame.Rect(115,325,771,120)
    global playGuestRect
    playGuestRect = pygame.Rect(115,325,353,120)
    global loginRect
    loginRect = pygame.Rect(533,325,353,120)
    global easyRect
    easyRect = pygame.Rect(115,325,353,120)
    global mediumRect
    mediumRect = pygame.Rect(533,325,353,120)
    global expertRect
    expertRect = pygame.Rect(115,465,770,120)
    global leaderboardRect
    leaderboardRect = pygame.Rect(115,465,771,120)

    global backButton
    backButton = pygame.Rect(50,50,50,50)

    clock = pygame.time.Clock()

    #Used to keep track of if user is on difficulty select screen
    global difficultySelect
    difficultySelect = False

    while True:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False,0,''

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.collidepoint(event.pos):
                    #Back button is only on difficulty screen, so put user back to main menu screen
                    difficultySelect = False


                #Main menu screen
                if not difficultySelect:
                    if USERNAME:
                        if playSignedInRect.collidepoint(event.pos):
                            difficultySelect = True
                    
                    else:
                        if playGuestRect.collidepoint(event.pos):
                            difficultySelect = True
                        elif loginRect.collidepoint(event.pos):
                            return True,2,''
                    
                    if leaderboardRect.collidepoint(event.pos):
                        return True,3,''


                #Difficulty select screen
                else:
                    if easyRect.collidepoint(event.pos):
                        return True,1,'Easy'
                    elif mediumRect.collidepoint(event.pos):
                        return True,1,'Medium'
                    elif expertRect.collidepoint(event.pos):
                        return True,1,'Expert'
        draw_board()




def draw_board():
    WIN.fill(BISQUE)
    WIN.blit(LOGO,(115,50))

    if not difficultySelect:
        if USERNAME:
            pygame.draw.rect(WIN,DARKBISQUE,playSignedInRect) #Play
            WIN.blit(FONT.render('PLAY',True,(0,0,0)),(400,335))
        
        else:
            pygame.draw.rect(WIN,DARKBISQUE,playGuestRect) #Play
            WIN.blit(FONT.render('PLAY',True,(0,0,0)),(210,335))
            pygame.draw.rect(WIN,DARKBISQUE,loginRect) #Login
            WIN.blit(FONT.render('LOGIN',True,(0,0,0)),(595,335))
        
        pygame.draw.rect(WIN,DARKBISQUE,leaderboardRect)
        WIN.blit(FONT.render('LEADERBOARD',True,(0,0,0)),(255,475))
        
    else:
        pygame.draw.rect(WIN,DARKBISQUE,easyRect) #Easy
        WIN.blit(FONT.render('EASY',True,(0,0,0)),(210,335))
        
        pygame.draw.rect(WIN,DARKBISQUE,mediumRect) #Medium
        WIN.blit(FONT.render('MEDIUM',True,(0,0,0)),(575,335))
        
        pygame.draw.rect(WIN,DARKBISQUE,expertRect) #Expert
        WIN.blit(FONT.render('EXPERT',True,(0,0,0)),(390,475))  

    if USERNAME:
        WIN.blit(USERNAME_FONT.render(USERNAME,True,(0,0,0)),(30,695))
    
    if difficultySelect:
        pygame.draw.rect(WIN,DARKBISQUE,backButton)
        WIN.blit(BACK,(backButton.x,backButton.y))

    pygame.display.update()
