from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# from email.mime.image import MIMEImage
# from email.mime.application import MIMEApplication
USERNAME = ""
PASSWORD = ""
SENDER = ""
class EmailClient():
    def __init__(self):
        self.__msg = MIMEMultipart()
        self.__msg.add_header("From", SENDER)
        __host = "smtp.gmail.com"
        __port = 587
        self.__server = smtplib.SMTP(__host, __port)
        


    def sendMail(self, recipient, subject, body):
        self.__server.starttls()
        self.__server.login(USERNAME, PASSWORD)
        self.__msg.add_header("Subject", subject)
        self.__msg.add_header("To", recipient)
        self.__msg.attach(MIMEText(body, "plain"))
        self.__server.send_message(self.__msg)
        self.__server.quit()
