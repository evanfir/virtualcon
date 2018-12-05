from flask import Flask
from flask_restful import Api, Resource, reqparse
from dbhandler import dbHandler
from emailHandler import EmailClient
from vcCrawler import VirtualCrawler


app = Flask(__name__)
api = Api(app)

studentDB = dbHandler("student", "student") #initiate studentDB
QuestionDB = dbHandler("qa", "qa") #initiate Question and Answers DB
SurveyDB = dbHandler("survey", "survey")

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


    def post(self):
        args = parser.parse_args()
        studentDB.insertStudentInfo(int(args['id']), args['first'], args['last'], args['major'])
        return args['id'], args['first'], args['last'], args['major'], 201
        

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
        if len(answer) > 0:
            return answer, 200
        else:
            return "Question not found", 404


## Admin API (child of StudentApi) allows admin to add, edit or retrieve a question and answer
# to call: /AdminApi?question=XXXXX&answer=XXXXX
class AdminApi(StudentApi):
    parser.add_argument('question')
    parser.add_argument('answer')
    def get(self):
        args = parser.parse_args()
        question = args["question"]
        if question is None:
            answer = QuestionDB.retrieveAnswer("*")
        else:
            answer = QuestionDB.retrieveAnswer(question)
        if len(answer) > 0:
            return answer, 200
        else:
            return "Question not found", 404


    def post(self):
        args = parser.parse_args()
        question = args['question']
        answer = args['answer']
        if question is not None and answer is not None:
            QuestionDB.insertQuestion(args['question'], args['answer'])
            return ("Question: ", args['question'], "Answer: ", args['answer']), 201
        else:
            return "Question or Answer or both are missing", 404

    def put(self):
        args = parser.parse_args()
        question = args['question']
        answer = args['answer']
        if question is not None and answer is not None:
            QuestionDB.updateQuestion(question, answer)
            return ("Question: ", question, "Answer: ", answer), 201
        else:
            return "Question or Answer or both are missing", 404


## Email client API handles emails student wanna send to the admin
# to call: /EmailApi?sender=XXXX&subject=XXXX&body=XXXX
# only has post interface
class EmailApi(Resource):
    parser.add_argument('sender')
    parser.add_argument('subject')
    parser.add_argument('body')
    
    def post(self):
        emailClient = EmailClient()
        args = parser.parse_args()
        sender = args['sender']
        subject = args['subject'] 
        body = args['body']
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
    
    def get(self):
        args = parser.parse_args()
        crawler = VirtualCrawler(args['to'])
        link = crawler.getiFrameLink()
        return link, 200


class SurveyApi(Resource):
    parser.add_argument("question")
    parser.add_argument("comment")
    parser.add_argument("id")
    
    def get(self):
        results = SurveyDB.retrieveSurveyResults()
        # print("\n\n")
        # print(results)
        # print("\n\n")
        return results, 200

    def post(self):
        args = parser.parse_args()
        rate = args['rate']
        comment = args['comment']
        studentID = args['id']
        if rate is None:
            rate = -1
        if comment is None:
            comment = "N/A"
        if studentID is None:
            studentID = 0
        SurveyDB.insertSurvey(rate, comment, studentID)
        return rate, comment, studentID, 201
        
api.add_resource(StudentInfo, "/StudentInfo")
api.add_resource(StudentApi, "/StudentApi")
api.add_resource(AdminApi, "/AdminApi")
api.add_resource(EmailApi, "/EmailApi")
api.add_resource(CrawlerApi, "/CrawlerApi")
api.add_resource(SurveyApi, "/SurveyApi")

def runFlask():
    app.run(debug=True)
