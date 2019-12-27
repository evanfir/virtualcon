"""
Virtual Counselor
Final Project 
CS 03C
Professor Ashraf
By: Evan Firoozi, Marcello Yapura
Email: afiroozi@go.pasadena.edu, myapura@go.pasadena.edu
December 2018

This class is a email client that allows the application 
to send email to counselor. 
Later this class can be expanded to receive emails from counselor 
and add them to the database directly or make changes to questions 
and answers.
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


USERNAME = "vc9038704@gmail.com"
PASSWORD = "z4PAPpF64b$"
# RECEIPIENT = "aa@bb.cc"

class EmailClient():
    def __init__(self):
        #make the MIME object for the header and body
        self.__msg = MIMEMultipart()
        self.__msg.add_header("To", USERNAME)
        self.__msg.add_header("From", USERNAME)
        __host = "smtp.gmail.com"
        __port = 587
        
        ##make the connection to the SMTP server
        self.__server = smtplib.SMTP(__host, __port)
        self.__server.starttls()
        
    ##send an email using the input data
    def sendMail(self, sender, subject, body):
        self.__msg.add_header("reply-to", sender)
        self.__server.login(USERNAME, PASSWORD)
        self.__msg.add_header("Subject", subject)
        self.__msg.attach(MIMEText(body, "plain"))
        #send email
        self.__server.send_message(self.__msg) 
        
        
        #close the connection
        self.__server.quit()
        # print("\n\nDEBUG: email sent \n\n")

def main():
    eclient = EmailClient()
    eclient.sendMail("aa@bb.cc", "whats up", "this is body")

# main()