"""
Core of the program
Run the program's in two modes:

i. with arg 'api': run the API of the program
ii. with arg 'vc' or None: run the GUI

"""
from myFlask import runFlask
from virtualcouncelor import run
from sys import argv


if argv[1] == "api":
    runFlask()
else:
    run()
