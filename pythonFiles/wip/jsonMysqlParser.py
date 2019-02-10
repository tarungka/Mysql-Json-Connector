import json
import import_logger

logger = import_logger.logIt(__file__)

class jsonConfiguration:
    path = None
    allData = {} #DICTIONARY CONTAINING ALL THE DATA
    allDatabases = []
    dataDictionary = {} #DICTIONARY "DATABASE_NAME" : "TABLE_NAME" 
    allTables = []
    databaseTableRelation = {}
    def __init__(self,path):
        self.path = path
        try:
            print("Opening file '%s' ..." % (path),end="")
            self.file = open(path)
            print("(success)")
            print("Loading json data ...",end="")
            self.allData = json.load(self.file)
            print("(success)")
            print("Searching for databases in the file ...",end="")
            self.allDatabases = list(self.allData["databases"].keys())
            print("(success)")
            print("Searching for tables in the file ...",end="")
            for database in self.allDatabases:
                self.dataDictionary.update({database : self.allData["databases"][database]["tables"].keys()})
            print("(success)")
            #databases = list(self.getDatabases())
            newtables = list(self.getRelation().values())
            for tableSet in newtables:
                for atable in tableSet:
            	    self.allTables.append(atable)
        except FileNotFoundError:
            print("The file does not exist.")
            print("Do you want to create it(Y/N)?",end='')
            value = input()
            while(value == None):
                value = input()
            print(value)
            if(value == "Y" or value == "y"):
                print("creating new file")
                self.createConfigFile()
            else:
                exit(0)

    def getInput(self,string,arg):
        if(type(arg) == list):
            arg.append(input(string))
        elif(type(arg) == str):
            arg = input(string)
        else:
            print("This datatype is not supported:%s" % str(type(arg)))
        return
        #if(arg == None):
        #    return False
        #else:
        #    return True

    def createConfigFile(self):
        self.getInput("Enter the path of the file:",self.path)
        #dbName = input("Enter the database name:")
        #if(dbName != None):
        #    self.allDatabases.append(dbName)
        print(self.path)
    def showAllData(self):
        print(self.path)
        print(self.allData)
        print(self.allDatabases)
        print(self.dataDictionary)

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


#test_object = jsonConfiguration("json/config_mysq.json")
#test_object.showAllData()
#test_object.createConfigFile()