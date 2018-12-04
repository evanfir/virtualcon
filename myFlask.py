from flask import Flask
from flask_restful import Api, Resource, reqparse
from dbhandler import *
from emailHandler import EmailClient

app = Flask(__name__)
api = Api(app)

studentDB = dbHandler("student", "student") #initiate studentDB
QuestionDB = dbHandler("qa", "qa") #initiate Question and Answers DB

parser = reqparse.RequestParser() 

#student handles everything about student includeing id, name, lname, major
#to call: /StudentInfo?id=000&first=XXXX&last=XXXX&major=XXXX
class StudentInfo(Resource):
    parser.add_argument('id')
    parser.add_argument('first')
    parser.add_argument('last')
    parser.add_argument('major')

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

## Admin API allows admin to add, edit or retrieve a question and answer
# to call: /AdminApi?question=XXXXX&answer=XXXXX
class AdminApi(Resource):
    parser.add_argument('question')
    parser.add_argument('answer')
    def get(self):
        args = parser.parse_args()

        question = args["question"]
        answer = QuestionDB.retrieveAnswer(question)
        if len(answer) > 0:
            return answer, 200
        else:
            return "Question not found", 404

    def post(self):
        args = parser.parse_args()

        QuestionDB.insertQuestion(args['question'], args['answer'])
        return ("Question: ", args['question'], "Answer: ", args['answer']), 201


    def put(self):
        args = parser.parse_args()

        QuestionDB.updateQuestion(args['question'], args['answer'])
        return ("Question: ", args['question'], "Answer: ", args['answer']), 201

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
        emailClient.sendMail(args['sender'], args['subject'], args['body'])
        return 201


api.add_resource(StudentInfo, "/StudentInfo")
api.add_resource(StudentApi, "/StudentApi")
api.add_resource(AdminApi, "/AdminApi")
api.add_resource(EmailApi, "/EmailApi")
def runFlask():
    app.run(debug=True)
