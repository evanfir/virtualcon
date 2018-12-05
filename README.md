# virtualcon

Student Virtual Counselor 

This program helps CS students to get information about their major, transfer requirements and etc directly from computer instead of an actual counselor. 

Program designed in a way that its use can expand to all other majors.

To improve the exprience, it gets the transfer information from assist.org and shows it to the student.

##Structure

This program is a multi parter and consists of:
dbHandler: to handle 3 databases
emailHandler: to send email to the counselor 
myFlask: holds all the APIs 
vcCrawler: that crawls assist.org for the information on transfer
survey: manages the final survey
GUI: we used JS and HTML/CSS as the programs UI

##database
We used sqlite3 for database. 

Currently we are managing 3 different databases:
1. Student info consists of student ID, first name, last name, and major

2. Question and Answer consists of questions and their relative answers

3. survey resutls that holds the results of the surveys that students fill

## how to run
To install requirements: 
    
    pip3 install -r requirements.txt

Then you can run the code with the below command:

    python3 core.py