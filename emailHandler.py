from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


USERNAME = "vc9038704@gmail.com"
PASSWORD = "z4PAPpF64b$"
# RECEIPIENT = "aa@bb.cc"

class EmailClient():
    def __init__(self):
        self.__msg = MIMEMultipart()
        self.__msg.add_header("To", USERNAME)
        self.__msg.add_header("From", USERNAME)
        __host = "smtp.gmail.com"
        __port = 587
        self.__server = smtplib.SMTP(__host, __port)
        self.__server.starttls()
        


    def sendMail(self, sender, subject, body):
        self.__msg.add_header("reply-to", sender)
        self.__server.login(USERNAME, PASSWORD)
        self.__msg.add_header("Subject", subject)
        self.__msg.attach(MIMEText(body, "plain"))
        self.__server.send_message(self.__msg)
        # print("\n\nDEBUG: email sent \n\n")
        self.__server.quit()


def main():
    eclient = EmailClient()
    eclient.sendMail("aa@bb.cc", "whats up", "this is body")

# main()