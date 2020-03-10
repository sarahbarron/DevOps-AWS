import re
import sys

def checkForExit(input):
    if re.search(r'^[eE][xX][iI][tT]$', input):
        sys.exit("\n\n Program exited before EC2 and S3 Bucket could be set up\n")
