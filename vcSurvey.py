"""
This class handles the survey for us. Currently 
the survey is consists of one rating, one comment, 
and student ID if its available.
"""

from dbhandler import dbHandler

##handles surveys 
#each survey has a rate, comment, and studentID

class Survey:
    def __init__(self):
        self.__surveydb = dbHandler("survey", "survey")

    ##add the input data into the database
    def addSurveyResult(self, rate, comment = " ", id = 000):
        self.__surveydb.insertSurvey(rate, comment, id)




        