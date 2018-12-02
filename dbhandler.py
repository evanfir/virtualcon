import sqlite3

class dbHandler:
    ## initialize a database
    # @param: database name without .db, dbtype: student/qa
    def __init__(self, dbname, dbtype):
        ## make a SQLite object
        __dbName = dbname + ".db"
        __conn = sqlite3.connect(dbname)
        __cursorObj = __conn.cursor()
        __dbtype = dbtype
        if __dbtype == "student":
            __columnNamesTypes = "StudentID int, FirstName TEXT, LastName TEXT, Major TEXT"
        if __dbtype == "qa":
            __columnNamesTypes = "ID INT, Question TEXT, Answer TEXT, KeyWords SET"
        __dbName = dbname + ".db"
        
        createStr = '''CREATE TABLE IF NOT EXISTS ''' + dbname + ''' (''' + __columnNamesTypes + ''');'''
        # createStr = '''CREATE TABLE student (StudentID int, FirstName TEXT);'''
        __cursorObj.execute(createStr)
        __conn.commit()
        __conn.close()
        print("done")

    ## insert question and answer to the database
    # @param: question str, answer str, keyWords set
    # check to make sure that dbtype is qa before proceeding
    def insertQuestion(self, question, answer, keyWords):
        if __dbtype == "qa":
            values = question + ", " + answer
            insertStr = "INSERT INTO " + __dbName + " (ID, Question, Answer, KeyWords) VALUES (" + values + ", " + keyWords + ");"
            __cursorObj.execute(insertStr)
            __conn.commit()

    # def makeKeywords(inputStr):

