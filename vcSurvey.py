from dbhandler import dbHandler

class Survey:
    def __init__(self):
        self.__surveydb = dbHandler("survey", "survey")

    def addSurveyResult(self, question, comment = " ", id = 000):
        self.__surveydb.insertSurvey(question, comment, id)

        


        