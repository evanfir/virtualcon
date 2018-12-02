from dbhandler import dbHandler

class Student:
    def __init__(self, studentID, firstName, lastName, major):
        self._studentID = studentID
        self._firstName = firstName
        self._lastName = lastName
        self._major = major
        