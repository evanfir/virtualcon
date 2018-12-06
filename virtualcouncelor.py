"""
This file is our appication's UI
Uses tkinter library
To use the GUI, call run() method
"""

from tkinter import *
# import tkinket as tk
from dbhandler import dbHandler
from emailHandler import EmailClient
from vcCrawler import VirtualCrawler

class VirtualCounselor(Frame):
    ## initializing the class
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        #initializing all databases
        self.answerdb = dbHandler("qa", "qa")
        self.surveyDB = dbHandler("survey", "survey")
        self.studentdb = dbHandler("student", "student")

    #initializing the main window
    def init_window(self):
        self.master.title("Virtual Councelor")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        self.makeLabel(0, 0)
        self.makeLabel(1, 1)
        self.makeLabel(2, 2, text = "Welcome To Virtual Councelor")
        self.makeLabel(3, 3)
        self.makeLabel(4, 4)
        self.makeLabel(5, 5)
        self.makeLabel(6, 5)
        #create main page buttons
        adminButton = Button(self, text="Administrator", command = self.clientAdmin, font=("Arial", 20))
        # adminButton.place(x=170, y=100)
        adminButton.grid(column = 2, row = 5)

        studentButton = Button(self, text="Student", command = self.studentInfoPage, font=("Arial", 20))
        # studentButton.place(x= 160, y = 150)
        studentButton.grid(column = 2, row = 6)

        self.createExitButton(2, 7)
    

    #make label for the main window
    def makeLabel(self, col, row, text = "  ", font=("Arial", 30)):
        lbl = Label(self, text=text, font = font)
        lbl.grid(column=col, row=row)

    #make label for any window other than main
    def makeLabelSub(self, tk, col, row, text = " ", font = ("Arial", 30)):
        lbl = Label(tk, text= text, font = font)
        lbl.grid(column = col, row = row)

    #Administrator main page
    # Admin can choose between:
    # Questions and Answers
    # Get Survey Results
    # Get Student Info
    def clientAdmin(self):
        # self.master.title("Administrator")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.adminTk = Tk()
        # allowing the widget to take the full space of the root window
        self.adminTk.geometry("400x600")
        # adminWindow = Window(self.adminTk)
        self.adminTk.title("Administrator Portal")
        
        self.makeLabelSub(self.adminTk, 1, 1, "Welcome to Admin Portal")
        self.makeLabelSub(self.adminTk, 0, 0)
        self.makeLabelSub(self.adminTk, 0, 2)
        self.makeLabelSub(self.adminTk, 0, 3)
        self.inLine = False # shows the answer in a seperate window
        addButton = Button(self.adminTk, text="Questions and Answers", command = self.addQuestionPage, font=("Arial", 20))
        # removeButton = Button(self.adminTk, text="Remove a Question", command = self.addQuestionPage, font=("Arial", 20))
        # editButton = Button(self.adminTk, text="Edit an Answer", command = self.addQuestionPage, font=("Arial", 20))
        surveyButton = Button(self.adminTk, text="Get Survey Results", command = self.retrieveSurvey, font=("Arial", 20))
        studentButton = Button(self.adminTk, text="Get Student Info", command = self.retrieveStudentPage, font=("Arial", 20))
        addButton.grid(column = 1, row = 4)
        # removeButton.grid(column = 1, row = 5)
        # editButton.grid(column = 1, row = 6)
        surveyButton.grid(column = 1, row = 6)
        studentButton.grid(column = 1, row = 8)
        self.adminTk.mainloop()

    # Question and Answer page for Admin
    # calls functions: submitQuestion, removeQuestion, editQuestion
    def addQuestionPage(self):
        self.addQuestionTk = Tk()
        self.addQuestionTk.geometry("700x400")
        # addQuestionWindow = Window(self.addQuestionTk)
        self.addQuestionTk.title("Add a Question and Answer")
        self.makeLabelSub(self.addQuestionTk, 0, 0)
        self.makeLabelSub(self.addQuestionTk, 1, 1, "Add a Question and Answer")
        self.makeLabelSub(self.addQuestionTk, 0, 2)
        self.makeLabelSub(self.addQuestionTk, 0, 3, "Question", font = ("Arial", 15))
        self.makeLabelSub(self.addQuestionTk, 0, 4, "Answer", font = ("Arial", 15))
        self.question = Entry(self.addQuestionTk, width = 60)
        self.answerEntry = Entry(self.addQuestionTk, width = 60)
        self.question.grid(column = 1, row = 3)
        self.answerEntry.grid(column = 1, row = 4)
        submitButton = Button(self.addQuestionTk, text="Submit", command = self.submitQuestion, font=("Arial", 20))
        submitButton.grid(column = 1, row = 6)
        removeButton = Button(self.addQuestionTk, text="Remove", command = self.removeQuestion, font=("Arial", 20))
        removeButton.grid(column = 1, row = 7)
        editButton = Button(self.addQuestionTk, text="Edit", command = self.editQuestion, font=("Arial", 20))
        editButton.grid(column =1, row = 8)
        answerButton = Button(self.addQuestionTk, text="Retrieve", command = self.getAnswer, font=("Arial", 20))
        answerButton.grid(column = 1, row = 9)
        self.addQuestionTk.mainloop()

    # submit question to the database
    def submitQuestion(self):
        question = self.question.get()
        answer = self.answerEntry.get()
        self.answerdb.insertQuestion(question, answer)
        self.makeLabelSub(self.addQuestionTk, 1, 10, "Question and Answer added")    

    # remove question from the database
    def removeQuestion(self):
        question = self.question.get()
        self.answerdb.deleteQuestion(question)
        self.makeLabelSub(self.addQuestionTk, 1, 10, "Question Removed")    

    # update a question in the database
    def editQuestion(self):
        question = self.question.get()
        answer = self.answerEntry.get()
        self.answerdb.updateQuestion(question, answer)
        self.makeLabelSub(self.addQuestionTk, 1, 10, "Question and Answer edited")

    # get all the surveys back
    def retrieveSurvey(self):
        retrieveSurveyTk = Tk()
        retrieveSurveyTk.geometry("400x500")
        # retrieveSurveyWindow = Window(retrieveSurveyTk)
        retrieveSurveyTk.title("Survey Results")
        self.makeLabelSub(retrieveSurveyTk, 1, 1, "Survey Results")
        self.makeLabelSub(retrieveSurveyTk, 0, 0)
        surveyResults = self.surveyDB.retrieveSurveyResults()
        self.makeLabelSub(retrieveSurveyTk, 0, 2, text = "ID:", font = ("Arial", 20))
        self.makeLabelSub(retrieveSurveyTk, 1, 2, text = "Rate:", font = ("Arial", 20))
        self.makeLabelSub(retrieveSurveyTk, 2, 2, text = "Comment:", font = ("Arial", 20))
            
        for i in range(len(surveyResults)):
            self.makeLabelSub(retrieveSurveyTk, 0, i + 3, text = str(surveyResults[i][0]), font = ("Arial", 10))
            self.makeLabelSub(retrieveSurveyTk, 1, i + 3, text = str(surveyResults[i][1]), font = ("Arial", 10))
            self.makeLabelSub(retrieveSurveyTk, 2, i + 3, text = str(surveyResults[i][2]), font = ("Arial", 10))
        retrieveSurveyTk.mainloop()    
        # print(surveyResults)

    # get all the students info back
    def retrieveStudentPage(self):
        retrieveStudentTk = Tk()
        retrieveStudentTk.geometry("600x500")
        # retrieveStudentWindow = Window(retrieveStudentTk)
        retrieveStudentTk.title("Survey Results")
        self.makeLabelSub(retrieveStudentTk, 2, 1, "Survey Results")
        self.makeLabelSub(retrieveStudentTk, 0, 0)
        studentInfo = self.studentdb.retrieveStudentInfo()
        self.makeLabelSub(retrieveStudentTk, 0, 2, text = "ID:", font = ("Arial", 20))
        self.makeLabelSub(retrieveStudentTk, 1, 2, text = "Name:", font = ("Arial", 20))
        self.makeLabelSub(retrieveStudentTk, 2, 2, text = "Last Name:", font = ("Arial", 20))
        self.makeLabelSub(retrieveStudentTk, 3, 2, text = "Major:", font = ("Arial", 20))
            
        for i in range(len(studentInfo)):
            self.makeLabelSub(retrieveStudentTk, 0, i + 3, text = str(studentInfo[i][0]), font = ("Arial", 10))
            self.makeLabelSub(retrieveStudentTk, 1, i + 3, text = str(studentInfo[i][1]), font = ("Arial", 10))
            self.makeLabelSub(retrieveStudentTk, 2, i + 3, text = str(studentInfo[i][2]), font = ("Arial", 10))
            self.makeLabelSub(retrieveStudentTk, 3, i + 3, text = str(studentInfo[i][3]), font = ("Arial", 10))

        retrieveStudentTk.mainloop() 
        
    # get student information and send them to the next window
    def studentInfoPage(self):
        studentInfoTk = Tk()
        studentInfoTk.geometry("400x300")
        # studentInfoWindow = Window(studentInfoTk)
        studentInfoTk.title("Enter your information")
        self.studentID = Entry(studentInfoTk, width = 10)
        self.studentName = Entry(studentInfoTk, width = 20)
        self.studentLName = Entry(studentInfoTk, width = 20)
        self.studentMajor = Entry(studentInfoTk, width = 20)
        idLable = Label(studentInfoTk, text="Student ID", font=("Arial", 20))
        nameLable = Label(studentInfoTk, text = "Name", font = ("Arial", 20))
        lNameLable = Label(studentInfoTk, text = "Last Name", font = ("Arial", 20))
        majorLabel = Label(studentInfoTk, text = "Major", font = ("Arial", 20))
        self.studentID.grid(row = 0, column = 1)
        self.studentName.grid(row = 1, column = 1)
        self.studentLName.grid(row = 2, column = 1)
        self.studentMajor.grid(row = 3, column = 1)
        idLable.grid(row = 0, column = 0)
        nameLable.grid(row = 1, column = 0)
        lNameLable.grid(row = 2, column = 0)
        majorLabel.grid(row = 3, column = 0)
        submitButton = Button(studentInfoTk, text="Submit", command = self.submitStudentInfo, font=("Arial", 20))
        submitButton.grid(column = 1, row = 4)
    
    # add the student info to the database
    def submitStudentInfo(self):
        studentID = self.studentID.get()
        name = self.studentName.get()
        lName = self.studentLName.get()
        major = self.studentMajor.get()
        self.studentdb.insertStudentInfo(studentID, name, lName, major)
        # self.studentTk.title("Student Portal")
        self.clientStudent()

    # main student client page
    def clientStudent(self):
        
        # self.master.title("Student Portal")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        
        self.studentTk = Tk()
        # allowing the widget to take the full space of the root window
        self.studentTk.geometry("800x400")
        # self.studentWindow = Window(self.studentTk)
        self.studentTk.title("Student Portal")
        # self.question = Entry(self.studentTk, width = 50)
        # questionLable = Label(self.studentTk, text="Question: ", font =("Arial", 20))
        self.makeLabelSub(self.studentTk, 0, 0)
        self.makeLabelSub(self.studentTk, 0, 1)
        self.makeLabelSub(self.studentTk, 0, 2)
        self.inLine = True ## shows the ansswer in the same window
        titleLable = Label(self.studentTk, text = "Student Portal", font =("Arial", 30))
        subTitleLable = Label(self.studentTk, text = "Ask your question or email counselor", font =("Arial", 30))
        titleLable.grid(column = 1, row = 0)
        subTitleLable.grid(column = 1, row = 1)
        
        # print("self.questionText: ", self.questionText)
        self.submitButton = Button(self.studentTk, text="Virtual Counselor", command = self.showQuestion, font=("Arial", 20))
        self.submitButton.grid(column = 2, row = 2)
        # submitButton.pack(side = TOP, expand=1)
        sendEmailButton = Button(self.studentTk, text="Send Email", command = self.sendEmail, font =("Arial", 20))
        sendEmailButton.grid(column = 2, row = 3)

        getTransferInfoButton = Button(self.studentTk, text="Transfer Info", command =self.showTransferWindow , font = ("Arial", 20))
        getTransferInfoButton.grid(column = 2, row = 4)

        self.studentTk.mainloop()

    # main transfer window
    def showTransferWindow(self):
        self.transferWindowTk = Tk()
        self.transferWindowTk.geometry("700x600")
        self.transferWindowTk.title("Transfer Information")
        self.var = IntVar()
        self.var.set(1)
        R1 = Radiobutton(self.transferWindowTk, text = "UCLA", variable = self.var, value = 1, command = self.showTransferInfo)
        # R1.pack( anchor = W )
        R1.grid(row = 2, column = 1)
        R2 = Radiobutton(self.transferWindowTk, text = "UC Irvine", variable = self.var, value = 2, command = self.showTransferInfo)
        # R2.pack( anchor = W )
        R2.grid(row = 3, column = 1)
        R3 = Radiobutton(self.transferWindowTk, text = "UC Berkeley", variable = self.var, value = 3,
                        command = self.showTransferInfo)
        # R3.pack( anchor = W)
        R3.grid(row = 4, column = 1)
        R4 = Radiobutton(self.transferWindowTk, text = "UC San Diego", variable = self.var, value = 4,
                        command = self.showTransferInfo)
        R4.grid(row = 5, column = 1)
        # R3.pack( anchor = W)
        # self.to = Entry(self.transferWindowTk, width = 50)
        # self.to.grid(column = 1, row = 2)
        # self.makeLabelSub(self.transferWindowTk, 1, 0, text = "Transfer Information")
        # self.makeLabelSub(self.transferWindowTk, 0, 0, text = "To: ", font =("Arial", 20))
        # self.submitButton.pack()
        # self.findButton = Button(self.transferWindowTk, text="submit", command = self.getAnswer, font=("Arial", 20))
        # self.findButton.grid(column = 2, row = 5)
        # self.option = var.get()
        # print("var: ", self.var.get())
        self.transferWindowTk.mainloop()

    # shows transfer info from assist.org in showTransferWindow
    def showTransferInfo(self):
        
        print(self.var.get())
        if  str(self.var.get()).lower() == "1":
            # print("ucla got called")
            ucla = VirtualCrawler("UCLA")
            ucla.getiFrameLink()
            plainText = ucla.getText()
            text = Text(self.transferWindowTk, bg = "Grey")
            text.insert(INSERT, plainText)
            text.grid(column = 1, row = 7)

            # text.pack()

    # show question and answer
    def showQuestion(self):
        self.question = Entry(self.studentTk, width = 50)
        self.questionLable = Label(self.studentTk, text="Question: ", font =("Arial", 20))
        self.questionLable.grid(column = 0, row = 6)
        self.question.grid(column = 1, row = 6)
        # self.submitButton.pack()
        self.findButton = Button(self.studentTk, text="Find Answer", command = self.getAnswer, font=("Arial", 20))
        self.findButton.grid(column = 2, row = 6)

    # send email to the counselor
    def sendEmail(self):
        self.sendEmailTk = Tk()
        self.sendEmailTk.geometry("700x200")
        # emailWindow = Window(self.sendEmailTk)
        self.sendEmailTk.title("Email Counselor")
        

        self.emailSubject = Entry(self.sendEmailTk, width = 20)
        self.sender = Entry(self.sendEmailTk, width = 20)
        self.emailBody = Entry(self.sendEmailTk, width = 50)
        self.emailSubject.grid(row = 0, column = 1)
        self.sender.grid(row = 1, column = 1)
        self.emailBody.grid(row = 2, column = 1)
        senderLable = Label(self.sendEmailTk, text="Email: ")
        subjectLable = Label(self.sendEmailTk, text="Subject: ")
        bodyLable = Label(self.sendEmailTk, text="Body: ")
        senderLable.grid(row = 1, column = 0)
        subjectLable.grid(row = 0, column = 0)
        bodyLable.grid(row = 2, column = 0)
        submitButton = Button(self.sendEmailTk, text = "Send", command=self.mailSent, font =("Arial", 30))
        submitButton.grid(row = 3, column = 1)
        self.sendEmailTk.mainloop()
        # self.sender.pack(side = RIGHT, expand=1)

    # email sent notification
    def mailSent(self):
        subject = self.emailSubject.get()
        sender = self.sender.get()
        body = self.emailBody.get()
        emailClient = EmailClient()
        emailClient.sendMail(sender, subject, body)
        sentVerify = Label(self.sendEmailTk, text = "Email Sent!")
        sentVerify.grid(row = 4, column = 1)

    # retrieve answer from the database
    def getAnswer(self):
        questionText = self.question.get()
        # print(self.questionText)
        answer = self.answerdb.retrieveAnswer(questionText)
        
        # text = Text(self, answer[0][0])
        # print(answer)
        
        if self.inLine == False:
            answerTk = Tk()
            answerTk.geometry("400x100")
            # answerWindow = Window(answerTk)
            answerTk.title(questionText)
            if len(answer) == 0:
                lbl = Label( answerTk, text="Question not found!")
            else:
                lbl = Label(answerTk, text=answer[0][0])
            lbl.pack(side = TOP, expand= 2)

            answerTk.mainloop()
        else:
            self.makeLabelSub(self.studentTk, 0, 8, text= "Answer: ")
            # self.answerText = Text(self.studentTk, bg = "Grey")
            # self.answerText.insert(INSERT, answer[0][0])
            # self.answerText.grid(column = 1, row = 8)
            if len(answer) == 0:
                lbl = Label(self.studentTk, text="Question not found!", bg = "Grey", font = ("Arial", 15))
            else:
                self.makeLabelSub(self.studentTk, 1, 8, text= answer[0][0], font = ("Arial", 15))

        # return text

    # exit button
    def createExitButton(self, x, y):
        # creating the quit button instance
        quitButton = Button(self, text="Exit",command=self.clientExit, font=("Arial", 20))

        # placing the button on my window
        quitButton.grid(column=x, row=y)

    # create menu
    def createMenu(self, master):
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.clientExit, font=("Arial", 20))

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")

        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)
    
    # exit the program
    def clientExit(self):
        exit()

    
def run():
    root = Tk()
    root.geometry("600x400")
    app = VirtualCounselor(root)
    app.init_window()
    root.mainloop()

# run()