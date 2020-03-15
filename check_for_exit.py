import re
import sys

def checkForExit(input):
    try:
        if re.search(r'^[eE][xX][iI][tT]$', input):
            sys.exit("\n\nProgram exited before the program could finish\n")
    except (Exception) as error:
        print(error)
    except(KeyboardInterrupt):
        sys.exit("\n\nProgram exited")
