import sqlite3
class dbHandler:
    QAID = 0
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
            values = str(dbHandler.QAID) + ", \"" + question + "\", \"" + answer + "\""
            insertStr = "INSERT INTO " + self._dbName + " (ID, Question, Answer) VALUES (" + values + ");"
            # print("DEBUG: insertStr: " + insertStr)
            self._cursorObj.execute(insertStr)
            self._conn.commit()
            self._conn.close()
            dbHandler.QAID = dbHandler.QAID + 1


    ## insert student info to the database
    # @params: studentID int, firstName str, lastName str, major str
    # check to make sure that dbtype is student before proceeding
    def insertStudentInfo(self, studentID, firstName, lastName, major):
        if self._dbtype == "student":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            values = str(studentID) + ",\"" + firstName + "\", \"" + lastName + "\", \"" + major + "\""
            insertStr = "INSERT INTO " + self._dbName + " (StudentID, FirstName, LastName, Major) VALUES (" + values + ");"
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
            values = "\"" + question + "\""
            selectStr = "SELECT Answer FROM " + self._dbName + " WHERE Question = " + values
            self._cursorObj.execute(selectStr)
            answer = self._cursorObj.fetchall()
            self._conn.close()
            return answer

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
    
    ## update answer
    # @params: question str, answer str
    def updateQuestion(self, question, answer):
        if self._dbtype == "qa":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            # values = "\"" + studentID + "\""
            selectStr = "UPDATE " + self._dbName + " SET Answer = \"" + answer + "\" WHERE Question = \"" + question + "\""
            print(selectStr)
            self._cursorObj.execute(selectStr)
            self._conn.commit()
            self._conn.close()

    ## update student info based on studentID
    # @params: studentID int, firstName str, lastName str, major str
    def updateStudentInfo(self, studentID, firstName, lastName, major):
        if self._dbtype == "student":
            self._conn = sqlite3.connect(self._dbName)
            self._cursorObj = self._conn.cursor()
            updateInfo = "UPDATE " + self._dbName + " SET FirstName = \"" + firstName + "\" WHERE StudentID = " + str(studentID)
            self._cursorObj.execute(updateInfo)

            updateInfo = "UPDATE " + self._dbName + " SET LastName = \"" + lastName + "\" WHERE StudentID = " + str(studentID)
            self._cursorObj.execute(updateInfo)

            updateInfo = "UPDATE " + self._dbName + " SET Major = \"" + major + "\" WHERE StudentID = " + str(studentID)
            self._cursorObj.execute(updateInfo)
            self._conn.commit()
            self._conn.close()

