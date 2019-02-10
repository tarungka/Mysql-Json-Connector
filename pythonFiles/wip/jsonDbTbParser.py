import json
import import_logger
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes

logger = import_logger.logIt(__file__)

class jsonConfiguration:
    path = None
    allData = {} #DICTIONARY CONTAINING ALL THE DATA
    allDatabases = []
    dataDictionary = {} #DICTIONARY "DATABASE_NAME" : "TABLE_NAME" 
    allTables = []
    databaseTableRelation = {}
    def __init__(self):
        self.path = "json/jsonDbTbParser.json"
        try:
            print("Opening file '%s' ..." % (self.path),end="")
            with open(self.path) as file:
                print("(success)")
                print("Loading Json data ...",end="")
                self.allData = json.load(file)
                print("(success)")
                return
        except FileNotFoundError:
            print("(failed)")
            print("The file does not exist.")
            print("Do you want to create it(Y/N)?",end='')
            value = input()
            while(value == None):
                value = input()
            print("value is: " + value)
            if(value == "Y" or value == "y"):
                self.getInput()
            else:
                exit(0)
        except:
            print("(failed)")

    def getInput(self):
        print("Creating new json file by the name %s ..." % (self.path))
        againDatabase = 'y'
        self.dataDictionary = {}
        currentDictionary = {}
        while(againDatabase == 'y'):
            currentDatabase = input("Enter the database name: ")
            self.allDatabases.append(currentDatabase)
            currentTable = "y"
            allCurrentTable = []
            while(currentTable != 'n'):
                currentTable = input("Enter the table name: ")
                if(currentTable == 'n'):
                    break
                self.allTables.append(currentTable)
                allCurrentTable.append(currentTable)
            currentDictionary.update({currentDatabase : allCurrentTable})
            print(currentDictionary)
            if(input("Do you want to create another database(y/n)?") != 'y'):
                self.databaseTableRelation = currentDictionary
                self.showAllData()
                self.encrypt()
                break
    
    def showAllData(self):
        print("Path: ",self.path)
        print("allData: ",self.allData)
        print("allDatabases: ",self.allDatabases)
        print("dataDictionary: ",self.dataDictionary)
        print("allTables: ",self.allTables)
        print("databaseTableRelation: ",self.databaseTableRelation)

    def encrypt(self):
        jsonEncryption = {}
        databases = self.databaseTableRelation.keys()
        for database in databases:
            tables = self.databaseTableRelation[database]
            for table in tables:
                print("FUCK THIS SHIT",table)
            encrypt = AES.new('b7061433023f48ecf254849b4df59745',AES.MODE_CBC,get_random_bytes(16))
            jsonEncryption.update({str(encrypt.encrypt(database.ljust(16))) : database})
        print(jsonEncryption)

    def getDatabases(self):
        return self.allDatabases
    def getRelation(self):
        return self.dataDictionary
    def getTables(self):
        return self.allTables
    def read(self):
        return self.allData
    def saveAs(self,path,jsonData):
        with open(path,"w") as outFile:
            outFile.write(jsonData)


test_object = jsonConfiguration()