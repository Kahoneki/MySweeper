import pygame
from MainMenu import *
from GameMenu import *
from AccountMenu import *
from LeaderboardMenu import *


#Initialisation
WIDTH,HEIGHT = 1000,750
pygame.font.init()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("MySweeper")

BISQUE = (242,210,189)

FPS = 30



def main():
    USERNAME = None

    run = True
    currentScene = 0 #Menu screen
    
    while run:

        match currentScene:
            case 0:
                run,currentScene,difficulty = MainMenu(WIN,FPS,USERNAME)
            case 1:
                run,currentScene = GameMenu(WIN,FPS,difficulty,USERNAME)
            case 2:
                run,currentScene,USERNAME = AccountMenu(WIN,FPS)
            case 3:
                run,currentScene = LeaderboardMenu(WIN,FPS,USERNAME)
    
    pygame.quit()

main()
