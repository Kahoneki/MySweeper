import pygame
from DBFunctions import *

#----PYGAME INITIALISATION AND VARIABLES----#

pygame.font.init()

FONT = pygame.font.SysFont('Comic Sans MS',56)
SMALL_FONT = pygame.font.SysFont('Comic Sans MS',40)

LOGO = pygame.transform.scale(pygame.image.load('Media/Logo.png'),(770,250))
BACK = pygame.image.load('Media/back.png')

BISQUE = (242,210,189)
DARKBISQUE = (242,174,128)
DARKERBISQUE = (242,134,88)

#Gets updated when the user attempts to login / register
attemptedLogin = False
attemptedRegistration = False

#----END OF PYGAME INITIALISATION AND VARIABLES----#




#Modified class from stack overflow - https://stackoverflow.com/questions/46390231
class InputBox():
    
    def __init__(self,x,y,w,h,defaultText,typedText='',displayText='|'): #displayText is used to display password as asterisks, for username field: typedText=displayTex[:=1]
        self.rect = pygame.Rect(x,y,w,h)
        self.color = DARKBISQUE
        self.defaultText = defaultText
        self.default_text_surface = FONT.render(defaultText,True,(0,0,0))
        self.typedText = typedText
        self.displayText = displayText
        self.active = False
    

    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        self.color = DARKERBISQUE if self.active else DARKBISQUE
        
        if event.type == pygame.KEYDOWN and self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE] and self.displayText != '|':
                self.typedText = self.typedText[:-1]
                self.displayText = self.displayText[:-2] + '|'
            else:
                if self.defaultText == "USERNAME" and len(self.typedText) < 16: #16 is the max length for a username
                    if event.unicode.isalnum():
                        newText = ''
                        newText += self.typedText + event.unicode
                        self.typedText = newText
                        self.displayText = newText + '|'
                elif self.defaultText == "PASSWORD" and len(self.typedText) < 20: #20 is the max length for a password
                    newText = ''
                    newText += self.typedText + event.unicode
                    self.typedText = newText
                    self.displayText = ''
                    for i in range(len(self.typedText)):
                        self.displayText += '*'
                    self.displayText += '|'


    def resize_self(self):
        textWidth, textHeight = FONT.size(self.displayText) #textHeight is redundant
        if self.active == False and len(self.displayText) == 1:
            width = 600
        else:
            width = max(600,textWidth+10)
        self.rect.w = width





def AccountMenu(_win,FPS):
    global WIN
    WIN = _win

    global loginPage
    loginPage = False
    global registerPage
    registerPage = False

    global loginRect1
    loginRect1 = pygame.Rect(115,325,353,120)
    global registerRect1
    registerRect1 = pygame.Rect(533,325,353,120)
    global backButton
    backButton = pygame.Rect(50,50,50,50)

    global loginBox
    loginBox = pygame.Rect(25,550,300,100)
    global registerBox
    registerBox = pygame.Rect(25,550,300,100)
    global usernameInput
    usernameInput = InputBox(25,150,300,100,'USERNAME')
    global passwordInput


    passwordInput = InputBox(25,350,300,100,'PASSWORD')
    global input_boxes
    input_boxes = [usernameInput,passwordInput]

    global attempted
    attempted = False
    global errorCode
    errorCode = False
    global isAdmin
    isAdmin = False
    

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)

        for _event in pygame.event.get():
            global event
            event = _event
            if event.type == pygame.QUIT:
                return False,0,None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.collidepoint(event.pos):
                        if loginPage or registerPage:
                            #User is on the login page or register page, so send them back to the main login/register page
                            loginPage,registerPage = False,False
                        else:
                            #User is on the main login/register page, so go back to main menu without providing a username
                            return True,0,None


                #Changing screen
                if not loginPage and not registerPage:
                    if loginRect1.collidepoint(event.pos):
                        loginPage = True
                        
                    elif registerRect1.collidepoint(event.pos):
                        registerPage = True


            #Checks every frame if user has submitted details. errorCode will be None if user hasn't submitted details or has submitted correct details
            if loginPage:
                attempted,errorCode,isAdmin = LoginPageLogic()
                if errorCode:
                    draw_board()
                    pygame.time.wait(2000)
                    return True,2,None
                
            if registerPage:
                
                attempted,errorCode = RegisterPageLogic()
                if errorCode:
                    draw_board()
                    pygame.time.wait(2000)
                    return True,2,None


            if loginPage or registerPage:
                if attempted and not errorCode:
                    #User has attempted to log in / register and has not encountered an errorCode (errorCode=None), so log them in.
                    print(f"Logged in as {usernameInput.typedText}!")
                    draw_board()
                    pygame.time.wait(2000)
                    return True,0,usernameInput.typedText


        draw_board()




#Runs every frame while on the login page screen
def LoginPageLogic():
    isAdmin = False
    global errorCode

    #Ensuring only one input box is active at a single time
    if input_boxes[0].active and input_boxes[1].active:
        input_boxes[1].active = False

    for input_box in input_boxes:
        input_box.event_handler(event)
        input_box.resize_self()

    if errorCode:
        return errorCode,False

    if event.type == pygame.MOUSEBUTTONUP:
        if loginBox.collidepoint(event.pos):
            #User has clicked the login button, so check if their input is valid
            errorCode,isAdmin = ValidateLogin(usernameInput.typedText,passwordInput.typedText) #Will return None if valid
            if errorCode:
                return True,errorCode,False
            else:
                return True,None,isAdmin
    
    return False,None,False






#Searches for entered details in database
def ValidateLogin(username,password):
    usernameFound = False
    passwordFound = False
    rows = LoadUsers("accountinfo")
    for i in range(len(rows)):
        if rows[i][0] == username:
            usernameFound = True
            if rows[i][1] == password:
                passwordFound = True
                index = i
    if not usernameFound:
        return 1,False
    elif not passwordFound:
        return 2,False
    else:
        return None,rows[index][2]




#Gets run every frame while on the register screen
def RegisterPageLogic():
    global errorCode

    if input_boxes[0].active and input_boxes[1].active:
        input_boxes[1].active = False

    for input_box in input_boxes:
        input_box.event_handler(event)
        input_box.resize_self()

    if event.type == pygame.MOUSEBUTTONUP:
        if registerBox.collidepoint(event.pos):
            #User has clicked the register button, so check if their input is valid
            errorCode = ValidateRegistration(usernameInput.typedText,passwordInput.typedText) #Will return None if valid
            if errorCode:
                return True,errorCode
            else:
                rows = LoadUsers("accountinfo")
                AddUserToAccounts(rows,usernameInput.typedText,passwordInput.typedText,0)
                SaveUsers("accountinfo",rows)
                return True,None
    
    return False,None




#Checks if submitted details fit the requirements
def ValidateRegistration(username,password):

    #Searching for username in database
    rows = LoadUsers("accountinfo")
    for user in rows:
        if user[0].lower() == username.lower():
            return 1
    
    if len(username) < 6:
        return 2

    if len(password) < 8:
        return 3
    
    if not any(num in password for num in ['1','2','3','4','5','6','7','8','9','0']):
        return 4
    
    elif not any(char in password for char in ['!','"','£','$','&','*','(',')','-','_','+','=',';',':'\
                                               ,'@','#','~','/','?']):
        return 5
    
    elif not any(char in password for char in [chr(i) for i in range(65,91)]): #Capital letters
        return 6
    
    else:
        return None
    



def draw_board():
    WIN.fill(BISQUE)
    if not loginPage and not registerPage:
        WIN.blit(LOGO,(115,50))
        pygame.draw.rect(WIN,DARKBISQUE,loginRect1) #Login
        WIN.blit(FONT.render('LOGIN',True,(0,0,0)),(180,335))
        pygame.draw.rect(WIN,DARKBISQUE,registerRect1) #Register
        WIN.blit(FONT.render('REGISTER',True,(0,0,0)),(545,335))
    
    else:
        if loginPage:
            pygame.draw.rect(WIN,DARKBISQUE,loginBox)
            WIN.blit(FONT.render('LOG IN',True,(0,0,0)),(loginBox.x+10,loginBox.y+10))       
            if errorCode:
                match errorCode:
                    case 1:
                        WIN.blit(SMALL_FONT.render("USERNAME NOT FOUND",True,(255,0,0)),(400,550))
                    case 2:
                        WIN.blit(SMALL_FONT.render("INCORRECT PASSWORD",True,(255,0,0)),(400,550))
            if attempted and not errorCode:
                WIN.blit(SMALL_FONT.render("LOGGED IN AS",True,(0,255,0)),(400,550))
                WIN.blit(SMALL_FONT.render(usernameInput.typedText,True,(0,255,0)),(400,600))
                if isAdmin:
                    WIN.blit(SMALL_FONT.render("(Admin)",True,(0,0,255)),(400,650))
                
            

        else: #Register Page
            pygame.draw.rect(WIN,DARKBISQUE,registerBox)
            WIN.blit(FONT.render('REGISTER',True,(0,0,0)),(registerBox.x+10,registerBox.y+10))
            if errorCode:
                #Draw corresponding error code to the screen
                match errorCode:
                    case 1:
                        WIN.blit(SMALL_FONT.render("USERNAME ALREADY TAKEN",True,(255,0,0)),(400,550))
                    case 2:
                        WIN.blit(SMALL_FONT.render("USERNAME MUST BE",True,(255,0,0)),(400,550))
                        WIN.blit(SMALL_FONT.render("> 6 CHARACTERS",True,(255,0,0)),(400,600))
                    case 3:
                        WIN.blit(SMALL_FONT.render("PASSWORD MUST BE",True,(255,0,0)),(400,550))
                        WIN.blit(SMALL_FONT.render("> 8 CHARACTERS",True,(255,0,0)),(400,600))
                    case 4:
                        WIN.blit(SMALL_FONT.render("PASSWORD MUST CONTAIN",True,(255,0,0)),(400,550))
                        WIN.blit(SMALL_FONT.render("AT LEAST 1 NUMBER",True,(255,0,0)),(400,600))
                    case 5:
                        WIN.blit(SMALL_FONT.render("PASSWORD MUST CONTAIN",True,(255,0,0)),(400,550))
                        WIN.blit(SMALL_FONT.render("AT LEAST 1 SPECIAL CHARACTER",True,(255,0,0)),(400,600))
                    case 6:
                        WIN.blit(SMALL_FONT.render("PASSWORD MUST CONTAIN",True,(255,0,0)),(400,550))
                        WIN.blit(SMALL_FONT.render("AT LEAST 1 CAPITAL LETTER",True,(255,0,0)),(400,600))
            if attempted and not errorCode:
                WIN.blit(SMALL_FONT.render("LOGGED IN AS",True,(0,255,0)),(400,550))
                WIN.blit(SMALL_FONT.render(usernameInput.typedText,True,(0,255,0)),(400,600))


        #Drawing user typed text to the input boxes
        for input_box in input_boxes:
            pygame.draw.rect(WIN,input_box.color,input_box.rect)
            if not input_box.active:
                if len(input_box.displayText) == 1: #Checking that username field is empty before using default text
                    WIN.blit(FONT.render(input_box.defaultText,True,(0,0,0)),(input_box.rect.x+10,input_box.rect.y+10))
                elif len(input_box.displayText) > 1:
                    WIN.blit(FONT.render(input_box.displayText[:-1],True,(0,0,0)),(input_box.rect.x+10,input_box.rect.y+10))
            else:
                WIN.blit(FONT.render(input_box.displayText,True,(0,0,0)),(input_box.rect.x+10,input_box.rect.y+10))
    

    pygame.draw.rect(WIN,DARKBISQUE,backButton)
    WIN.blit(BACK,(backButton.x,backButton.y))
    
    
    pygame.display.update()
