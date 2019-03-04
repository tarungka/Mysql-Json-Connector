#!/usr/bin/python3
import json
import os

class test:

    def __init__(self):
        self.a = 10
        print(self.a)
    
    def showVaribale(self):
        self.a = 100
        print(self.a)

if __name__ == "__main__":
    os.system("./newdatabase.py")
    #process = test()
    #process.showVaribale()
else:
    print("Error")
