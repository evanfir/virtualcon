"""
Virtual Counselor
Final Project 
CS 03C
Professor Ashraf
By: Evan Firoozi, Marcello Yapura
Email: afiroozi@go.pasadena.edu, myapura@go.pasadena.edu
December 2018

Core of the program
Run the program's in two modes:

i. with arg 'api': run the API of the program
ii. with arg 'gui' or None: run the GUI

"""
from myFlask import runFlask
from virtualcouncelor import run
from sys import argv


if argv[1] == "api":
    runFlask()
else:
    run()
