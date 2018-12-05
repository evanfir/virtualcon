from flask import Flask
from flask_restful import Api, Resource, reqparse
from dbhandler import dbHandler
from emailHandler import EmailClient
from vcCrawler import VirtualCrawler


app = Flask(__name__)
api = Api(app)

studentDB = dbHandler("student", "student") #initiate studentDB
QuestionDB = dbHandler("qa", "qa") #initiate Question and Answers DB
SurveyDB = dbHandler("survey", "survey") #initiate Survey database

parser = reqparse.RequestParser() 

#student handles everything about student includeing id, name, lname, major
#to call: /StudentInfo?id=000&first=XXXX&last=XXXX&major=XXXX
class StudentInfo(Resource):
    parser.add_argument('id')
    parser.add_argument('first')
    parser.add_argument('last')
    parser.add_argument('major')

    ## send a get request with the id
    # @return: if success: info(json object) 
    #          else: 404
    def get(self): 
        args = parser.parse_args()
        studentID = args["id"]
        # print("\n\n\nstudentID: " + str(studentID) + "\n\n")
        info = studentDB.retrieveStudentInfo(int(studentID))
        if len(info) > 0:
            return info, 200
        else:
            return "Student Not Found", 404

    ## insert a student info into the db
    # @return: all the student info that from input and 201 for success
    def post(self):
        args = parser.parse_args()
        studentDB.insertStudentInfo(int(args['id']), args['first'], args['last'], args['major'])
        return args['id'], args['first'], args['last'], args['major'], 201
        
    ## update a student info
    # @return: all the student info that from input and 201 for success
    def put(self):
        args = parser.parse_args()
        studentDB.updateStudentInfo(int(args['id']), args['first'], args['last'], args['major'])
        return args['id'], args['first'], args['last'], args['major'], 201


## student API can only retrieve a question's answer
# to call: /StudentApi?question=XXXX XXXX
class StudentApi(Resource):
    parser.add_argument('question')
    def get(self):
        args = parser.parse_args()
        question = args["question"]
        answer = QuestionDB.retrieveAnswer(question)
        #check if any of the fields are NoneType
        if len(answer) > 0:
            return answer, 200
        else:
            return "Question not found", 404


## Admin API (child of StudentApi) allows admin to add, edit or retrieve a question and answer
# to call: /AdminApi?question=XXXXX&answer=XXXXX
class AdminApi(StudentApi):
    parser.add_argument('question')
    parser.add_argument('answer')

    ## get request
    # @return: answer to the question or error if question not found
    def get(self):
        args = parser.parse_args()
        question = args['question']
        answer = args['answer']
        #check if any of the fields are NoneType
        if question is None:
            answer = QuestionDB.retrieveAnswer("*")
        else:
            answer = QuestionDB.retrieveAnswer(question)
        if len(answer) > 0:
            return answer, 200
        else:
            return "Question not found", 404

    # Insert into the db
    # @return: question and answer that are added to the db
    def post(self):
        args = parser.parse_args()
        question = args['question']
        answer = args['answer']
        #check if any of the fields are NoneType
        if question is not None and answer is not None:
            QuestionDB.insertQuestion(args['question'], args['answer'])
            return ("Question: ", args['question'], "Answer: ", args['answer']), 201
        else:
            return "Question or Answer or both are missing", 404

    ## update entry
    # @return: question and answer that has been changed or 404 if either is missing
    def put(self):
        args = parser.parse_args()
        question = args['question']
        answer = args['answer']
        #check if any of the fields are NoneType
        if question is not None and answer is not None:
            QuestionDB.updateQuestion(question, answer)
            return ("Question: ", question, "Answer: ", answer), 201
        else:
            return "Question or Answer or both are missing", 404
    
    ## delete a question and answer
    # @return: 202 for success, 404 for failure
    def delete(self):
        args = parser.parse_args()
        question = args['question']
        if question is not None:
            QuestionDB.deleteQuestion(question)
            return 202
        else:
            return "Question not found", 404




## Email client API handles emails student wanna send to the admin
# to call: /EmailApi?sender=XXXX&subject=XXXX&body=XXXX
# only has post interface
class EmailApi(Resource):
    parser.add_argument('sender')
    parser.add_argument('subject')
    parser.add_argument('body')
    
    ## send an email 
    # @return 201 for success
    def post(self):
        emailClient = EmailClient()
        args = parser.parse_args()
        sender = args['sender']
        subject = args['subject'] 
        body = args['body']
        #check if any of the fields are NoneType
        if sender is None:
            sender = "N/A"
        if subject is None:
            subject = "N/A"
        if body is None:
            body = "N/A"
        emailClient.sendMail(sender, subject, body)
        return 201


## VCrawler is the interface of vcCrawler class
# to call: /VCrawler?to=XXXX
# currently only supports: UCB, UCI, UCD, and UCLA
# only has get and returns a link to an iFrame HTML page
class CrawlerApi(Resource):
    parser.add_argument("to")
    
    ## get the link to the iframe from assist.org
    # @return: a link
    def get(self):
        args = parser.parse_args()
        crawler = VirtualCrawler(args['to'])
        link = crawler.getiFrameLink()
        return link, 200

## SurveyApi is the VSurvey class
# to call: /SurveyApi?rate=5&comment=XXXX&id=000
# get returns all the db
# post insert a new row to the db
class SurveyApi(Resource):
    parser.add_argument("rate")
    parser.add_argument("comment")
    parser.add_argument("id")
    
    ## get all the survey results
    # @return: json
    def get(self):
        results = SurveyDB.retrieveSurveyResults()
        # print("\n\n")
        # print(results)
        # print("\n\n")
        return results, 200

    ## store a new survey result in db
    # @return: entry and 201 for success
    def post(self):
        args = parser.parse_args()
        rate = args['rate']
        comment = args['comment']
        studentID = args['id']
        #check if any of the fields are NoneType
        if rate is None:
            rate = -1
        if comment is None:
            comment = "N/A"
        if studentID is None:
            studentID = 0
        SurveyDB.insertSurvey(rate, comment, studentID)
        return rate, comment, studentID, 201

##handle arguments        
api.add_resource(StudentInfo, "/StudentInfo")
api.add_resource(StudentApi, "/StudentApi")
api.add_resource(AdminApi, "/AdminApi")
api.add_resource(EmailApi, "/EmailApi")
api.add_resource(CrawlerApi, "/CrawlerApi")
api.add_resource(SurveyApi, "/SurveyApi")

##run the flask
def runFlask():
    app.run(debug=True)
