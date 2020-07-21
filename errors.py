#!/usr/bin/python3
import logging
import os
import sys

PATH = None
pathToExeFromCurDir = sys.argv[0]
current_directory = os.getcwd()
if(pathToExeFromCurDir.startswith("/")):
    PATH = pathToExeFromCurDir
elif(pathToExeFromCurDir.startswith(".")):
    PATH = current_directory + pathToExeFromCurDir[1:]
else:
    PATH = current_directory + "/" + pathToExeFromCurDir
PATH = PATH.rsplit("/",1)[0] + "/"

logging.basicConfig(
    filename= PATH+'application.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


class UserDefinedError(Exception):
    """Writing user defined errors"""

    def __init__(self, errorString):
        """Write documentation for this"""
        logging.critical(errorString)
        print(errorString)
        exit(0)


class InsufficientDataError(Exception):
    """Called when there is insufficient data passed to the class"""

    def __init__(self):
        self.showError()
        return

    def showError(self):
        print("Insufficient data passed")


class NonCriticalError(Exception):
    """Called when there is an error from mysql but is not critical"""

    def __init__(self, errorMessage):
        logging.warning(errorMessage)
        print(errorMessage)

class UnknownDatabaseError(Exception):
    """Called when database does not exits"""

    def __init__(self,errorMessage=None):
        if(errorMessage):
            logging.warning(errorMessage)

if __name__ == "__main__":
    pass
else:
    pass