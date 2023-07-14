import mariadb

query1 = "select * from accountinfo"
query2 = "insert into accountinfo(Username,Password,isAdmin) values('p1','p2',p3)"
query3 = "delete from accountinfo where Username = p1"

query4 = "select * from leaderboard"
query5 = "insert into leaderboard(Username,HighScore,Difficulty) values('p1','p2','p3')"
query6 = "update leaderboard set HighScore = 'p1' WHERE HighScoreID='p2'"
query7 = "delete from leaderboard where HighScoreID = p1"

#Used to reset autoincrement HighScoreID
query8 = "ALTER TABLE `leaderboard` DROP `HighScoreID`"
query9 = "ALTER TABLE `leaderboard` ADD `HighScoreID` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST"


def DatabaseConnect():
  conn = mariadb.connect(
    host="localhost",
    user="root",
    passwd="newrootpassword",
    database="minesweeper"
    )
  return conn


def Query(queryString):
  try:
    conn = DatabaseConnect()
  except mariadb.Error as err:
    print("Error: Problem with database connection", err)
    
  else:
    cursor = conn.cursor()
    cursor.execute(queryString)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def LoadUsers(table):
  if table == "accountinfo":
    rows = Query(query1)
  else:
    rows = Query(query4)
  return(rows)

  
def AddUserToAccounts(rows,USERNAME,PASSWORD,isAdmin):
  myTuple = (0,USERNAME,PASSWORD,isAdmin)
  rows.append(myTuple)


#For Testing Purposes
def PrintUsers(rows):
  for i in range(len(rows)):
    print(rows[i])


def SaveUserFirstHighScore(USERNAME,SCORE,DIFFICULTY):
  conn = DatabaseConnect()
  cursor = conn.cursor()

  #Resetting auto increment
  cursor.execute(query8)
  cursor.execute(query9)
  conn.commit()

  saveQuery = query5.replace('p1',USERNAME)
  saveQuery = saveQuery.replace('p2',str(SCORE))
  saveQuery = saveQuery.replace('p3',DIFFICULTY)

  cursor.execute(saveQuery)
  conn.commit()
  conn.close()


def UpdateHighScore(rows,ID,NEWSCORE):
  conn = DatabaseConnect()
  cursor = conn.cursor()
  index = ID-1
  rows[index] = list(rows[index])
  updateQuery = query6.replace('p1',str(NEWSCORE))
  updateQuery = updateQuery.replace('p2',str(ID))

  cursor.execute(updateQuery)
  conn.commit()
  conn.close()


def SaveUsers(table,rows):
  conn = DatabaseConnect()
  cursor = conn.cursor()

  for i in range(len(rows)):
    if rows[i][0] == 0:
      saveQuery = query2.replace('p1',rows[i][1])
      saveQuery = saveQuery.replace('p2',str(rows[i][2]))
      saveQuery = saveQuery.replace('p3',str(rows[i][3]))

      cursor.execute(saveQuery)
  conn.commit()
  conn.close()


def DeleteUser(table,UID):
  conn = DatabaseConnect()
  cursor = conn.cursor()

  if table == "accountInfo":
    delQuery = query3.replace('p1',str(UID))
    cursor.execute(delQuery)
  else:
    delQuery = query7.replace('p1',str(UID))
    cursor.execute(delQuery)
    #Resetting auto-increment field
    cursor.execute(query8)
    cursor.execute(query9)
  
  
  conn.commit()
  conn.close()


def AdminCheck(USERNAME):
  rows = LoadUsers("accountinfo")
  for user in rows:
    if user[0] == USERNAME:
      return bool(user[2])
