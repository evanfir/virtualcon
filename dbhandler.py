import sqlite3
# import json

class dbHandler:
    ## initialize a database
    # @params: database name without .db, dbtype: student/qa
    def __init__(self, dbname, dbtype):
        ## make a SQLite object
        self._dbName = dbname
        self._conn = sqlite3.connect(dbname)
        self._cursorObj = self._conn.cursor()
        self._dbtype = dbtype
        if self._dbtype == "student":
            self._columnNamesTypes = "StudentID int, FirstName TEXT, LastName TEXT, Major TEXT"
        if self._dbtype == "qa":
            self._columnNamesTypes = "ID INT, Question TEXT, Answer TEXT"
        if self._dbtype == "survey":
            self._columnNamesTypes = "ID INT, Question1 TEXT, Comment TEXT"
        
        createStr = '''CREATE TABLE IF NOT EXISTS ''' + dbname + ''' (''' + self._columnNamesTypes + ''');'''
        # createStr = '''CREATE TABLE student (StudentID int, FirstName TEXT);'''
        self._cursorObj.execute(createStr)
        self._conn.commit()
        self._conn.close()
        # print("done")


    ## insert question and answer to the database
    # @params: question str, answer str
    # check to make sure that dbtype is qa before proceeding
    def insertQuestion(self, question, answer):
        if self._dbtype == "qa":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            
            # get the last entry's ID
            self._cursorObj.execute("SELECT ID FROM " + self._dbName + " order by ID DESC LIMIT 1")
            QAID = self._cursorObj.fetchall()
            if QAID is None:
                QAID = 0
            else:
                QAID = QAID[0][0] + 1
            # print("\nQAID: ", QAID, "\n")
            values = str(QAID) + ", \"" + question + "\", \"" + answer + "\""
            insertStr = "INSERT OR REPLACE INTO " + self._dbName + " (ID, Question, Answer) VALUES (" + values + ");"
            # print("DEBUG: insertStr: " + insertStr)
            self._cursorObj.execute(insertStr)
            self._conn.commit()
            self._conn.close()


    ## retrieve answer of a question
    # @params: question str
    # @return: answer: a list of a single set with 1 value
    def retrieveAnswer(self, question):
        if self._dbtype == "qa":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            
            if question is not '*':
                values = "\"" + question + "\""
                selectStr = "SELECT Answer FROM " + self._dbName + " WHERE Question = " + values
            else:
                selectStr = "SELECT * FROM " + self._dbName
            self._cursorObj.execute(selectStr)
            answer = self._cursorObj.fetchall()
            self._conn.close()
            return answer

    ## update answer
    # @params: question str, answer str
    def updateQuestion(self, question, answer):
        if self._dbtype == "qa":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            # values = "\"" + studentID + "\""
            selectStr = "INSERT OR REPLACE INTO " + self._dbName + " SET Answer = \"" + answer + "\" WHERE Question = \"" + question + "\""
            # print(selectStr)
            self._cursorObj.execute(selectStr)
            self._conn.commit()
            self._conn.close()

    ## delete a question and its answer
    # @param: question str
    def deleteQuestion(self, question):
        if self._dbtype == "qa":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            # values = "\"" + studentID + "\""
            selectStr = "DELETE FROM " + self._dbName + " WHERE Question = \"" + question + "\""
            # print(selectStr)
            self._cursorObj.execute(selectStr)
            self._conn.commit()
            self._conn.close()

    ## insert student info to the database
    # @params: studentID int, firstName str, lastName str, major str
    # check to make sure that dbtype is student before proceeding
    def insertStudentInfo(self, studentID, firstName, lastName, major):
        if self._dbtype == "student":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            values = str(studentID) + ",\"" + firstName + "\", \"" + lastName + "\", \"" + major + "\""
            insertStr = "INSERT OR REPLACE INTO " + self._dbName + " (StudentID, FirstName, LastName, Major) VALUES (" + values + ");"
            self._cursorObj.execute(insertStr)
            self._conn.commit()
            self._conn.close()

    
    ## retrieve student info of a studentID
    # @params: studentID int
    # @return: studentInfo: a set of 3 values: firstName, LastName, Major
    def retrieveStudentInfo(self, studentID):
        if self._dbtype == "student":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            # values = "\"" + studentID + "\""
            selectStr = "SELECT FirstName, LastName, Major FROM " + self._dbName + " WHERE StudentID = " + str(studentID)
            self._cursorObj.execute(selectStr)
            info = self._cursorObj.fetchall()
            self._conn.close()
            return info


    ## update student info based on studentID
    # @params: studentID int, firstName str, lastName str, major str
    def updateStudentInfo(self, studentID, firstName, lastName, major):
        if self._dbtype == "student":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            values = str(studentID) + ",\"" + firstName + "\", \"" + lastName + "\", \"" + major + "\""
            updateInfo = "INSERT OR REPLACE INTO " + self._dbName + " (StudentID, FirstName, LastName, Major) VALUES (" + values + ");"
            self._cursorObj.execute(updateInfo)
            self._conn.commit()
            self._conn.close()


    ## insert survey resutls to the database
    # @params: question1 str, comment str, id int
    # check to make sure that dbtype is survey before proceeding
    def insertSurvey(self, rate, comment = " ", id = 000):
        if self._dbtype == "survey":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            values = str(id) + ", \"" + rate + "\", \"" + comment + "\""
            insertStr = "INSERT INTO " + self._dbName + " (ID, Rate, Comment) VALUES (" + values + ");"
            # print("DEBUG: insertStr: " + insertStr)
            self._cursorObj.execute(insertStr)
            self._conn.commit()
            self._conn.close()

    ## retrieve all the survey results
    # @return: a json view of all the results
    def retrieveSurveyResults(self):
        if self._dbtype == "survey":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            retrieveStr = "SELECT * FROM " + self._dbName
            self._cursorObj.execute(retrieveStr)
            returnStr = self._cursorObj.fetchall()
            self._conn.commit()
            self._conn.close()

            return returnStr