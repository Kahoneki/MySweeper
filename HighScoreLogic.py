from DBFunctions import *

def GetUserHighScore(USERNAME,DIFFICULTY):
    rows = LoadUsers("leaderboard")
    for user in rows:
        if USERNAME == user[1] and DIFFICULTY == user[3]:
            return user[2]
    return None




def UpdateUserHighScore(USERNAME,DIFFICULTY,NEWHIGHSCORE):
    rows = LoadUsers("leaderboard")
    for ID,user in enumerate(rows):
        if user[1] == USERNAME and user[3] == DIFFICULTY:
            UpdateHighScore(rows,ID+1,NEWHIGHSCORE) #ID+1 since auto-increment starts at 1
            return
    SaveUserFirstHighScore(USERNAME,NEWHIGHSCORE,DIFFICULTY)




def DeleteUserHighScore(USERNAME,DIFFICULTY): #For Admins Only
    rows = LoadUsers("leaderboard")
    for i,user in enumerate(rows):
        if USERNAME == user[1] and DIFFICULTY == user[3]:
            DeleteUser("leaderboard",i+1) #Since HighScoreID starts at 1
            return




def CheckNewHighScore(USERNAME,DIFFICULTY,HIGH_SCORE):
    rows = LoadUsers("leaderboard")
    for hs in rows:
        if USERNAME == hs[1] and DIFFICULTY == hs[3]:
            return HIGH_SCORE < hs[2] #High score represented as number of seconds taken to complete - lower is better
    return True #User doesn't have a high score for `DIFFICULTY` yet