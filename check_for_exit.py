import re
import sys

def checkForExit(input):
    if re.search(r'^[eE][xX][iI][tT]$', input):
        sys.exit("\n\nProgram exited before the program could finish\n")
