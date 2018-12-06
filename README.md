# virtualcon

Student Virtual Counselor 

This program helps CS students to get information about their major, transfer requirements and etc directly from computer instead of an actual counselor. 

Program designed in a way that its use can expand to all other majors.

To improve the exprience, it gets the transfer information from assist.org and shows it to the student.

## how to install and run

To install requirements: 
    
    pip3 install -r requirements.txt

Then you can run the program in two states:

1. To access application API

    python3 core.py api

2. To show the GUI window and application UI

    python3 core.py
    python3 core.py gui

## how to use API

Go to myFlask

Uses restfull flask standard API interface

## how to use GUI/UI

See to the visualManual.pdf

## Structure

This program is a multi parter and consists of:
dbHandler: to handle 3 databases
emailHandler: to send email to the counselor 
myFlask: holds all the APIs 
vcCrawler: that crawls assist.org for the information on transfer
vcSurvey: manages the final survey
GUI: we used JS and HTML/CSS as the programs UI


## database / dbHandler

We used sqlite3 for database. 

Currently we are managing 3 different databases:
1. Student info consists of student ID, first name, last name, and major

2. Question and Answer consists of questions and their relative answers

3. survey resutls that holds the results of the surveys that students fill

## emailHandler

This class is a email client that allows the application to send email to counselor. 

Later this class can be expanded to receive emails from counselor and add them to the database directly or make changes to questions and answers.

## myFlask / flask_restful

This file is the main interface of the backend of the program. We used flask restful as an standard API that can be used in other programs later.

In this file, we have several classes as below:

### StudentInfo

StudentInfo is the database interface for student information including student id, first and last name, and major.

This class has get, post, and put methods.

general call:
    
    /StudentInfo?id=000&first=XXXX&last=XXXX&major=XXXX

### StudentApi

This class is the student interface for the question and answer database and does not let student edit/add or delete question or answers.

general call:

    /StudentApi?question=XXXX XXXX

### AdminApi

AdminApi class is a subclass of StudentApi with more functionality. it has post, put, and delete functions as well that allows the system admin edit the database of the questions and answers

general call:

    /AdminApi?question=XXXXX&answer=XXXXX

### EmailApi

This class is our email client's interface. Currently it only has post method that let a student send an email to the counselor.

general call:

    /EmailApi?sender=XXXX&subject=XXXX&body=XXXX

### CrawlerApi

This class is our crawler's interface and currently only has get method.

general call: 
    
    /CrawlerApi?to=XXXX

### SurveyApi

This class is the programs survey class interface and has get and post methods. 

get method returns all the survey's results from the database.

general call:

    /SurveyApi?rate=5&comment=XXXX&id=000

## vcCrawler

This is the first version of our crawler that crawls assist.org to get information on courses that are necessary for each CS student prior to transfer to a 4 year university. 

Currently this program only can retrieve information for PCC students that wanna transfer to UCI, UCD, UCSD, and UCLA.

For future, this program can be expanded to other schools and universities and majors.

## vcSurvay

This class handles the survey for us. Currently the survey is consists of one rating, one comment, and student ID if its available.

## virtualcouncelor

VirtualCounselor class controls the GUI and uses tkinter library for that purpose.
This class calls functions from dbHandler, EmailClient, and VirtualCrawler

### init_window

initializing the main window

### makeLabel

make label for the main window

### makeLabelSub

make label for any window other than main

### clientAdmin

Administrator main page
Admin can choose between:
Questions and Answers
Get Survey Results
Get Student Info

### addQuestionPage

Question and Answer page for Admin
calls functions: submitQuestion, removeQuestion, editQuestion

### submitQuestion

submit question to the database

###removeQuestion

remove question from the database

### editQuestion

update a question in the database

### retrieveSurvey

get all the surveys back

### retrieveStudentPage

get all the students info back

### studentInfoPage

get student information and send them to the next window


### submitStudentInfo

add the student info to the database

### clientStudent

main student client page

### showTransferWindow

main transfer window

### showTransferInfo

shows transfer info from assist.org in showTransferWindow

### showQuestion

show question and answer

### sendEmail

send email to the counselor

### mailSent

email sent notification

### getAnswer

retrieve answer from the database

### createExitButton

exit button

### createMenu

creates menu

### clientExit

Terminates the program





