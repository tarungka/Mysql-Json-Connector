#!/usr/bin/python3
import mysqlConnector as sql
import json
import userDefinedFunctions as userFunctions

class analytics:
    def __init__(self,connection,**kwargs):
        #Write code here to load the data
        self.connection = connection
        # self.cursor = cursor
        self.args = kwargs
        #print("Constructor")
        try:
            with open(".config/extraData.json") as cnfFile:
            	self.jsonData = json.load(cnfFile)
        except FileNotFoundError:
            ans = input("File does not exit, do you want to create it?(y/n)")
            if(ans == 'y' or ans == 'Y'):
                print("Write code to create a new file.")
                exit(0)
            else:
                exit(0)
        except Exception as e:
            print("Unhandeled Error...exitting...",str(e))
            exit()

    def showData(self):
    	print("json data:",self.jsonData)

    def loadData(self,data):
        self.select = data["select"]
        self.update = data["update"]
        print("select",self.select)
        print("update",self.update)

    def returnAsString(self,*args):
        print("Type:",type(args))
        for element in args:
            if(type(element) is dict):
                for x in element:
                    print("--->",x,element[x],element[x].strftime("%d-%m-%y"),type(element[x])) #Add the string format
                    return element[x].strftime("%Y-%m-%d %H:%M:%S")
            else:
                print("Is not supported")

    def processSetCondition(self,inputList):
        returnDict = {}
        print(inputList)
        for element in inputList:
            #print(element)
            if("=" in element):
                key,val = element.split("=")
                if("select" in val):
                    # print("val",val)
                    indexNo = val.split("[")[1]
                    indexNo = indexNo.split("]")[0]
                    if(self.selectResponse[int(indexNo)]):
                        #print(val,indexNo)
                        val = self.returnAsString(self.selectResponse[int(indexNo)][0])   #ALWAYS TAKES INDEX 0, CANNOT HANDLE MORE THAN ONE RESPONSE
                    else:
                        print("No data got from database for '{}' key!".format(key))
                returnDict.update({key:val})
        print("returnDict",returnDict)
        return returnDict

    def generateAnalytics(self,case=None):
        self.selectResponse = []
        if(case):
            self.loadData(self.jsonData[case])
            if(self.select):
                # print("---",self.select,"---")
                for selectData in self.select:
                    print(selectData)
                    if(selectData["passed_by_another_script"] == False):
                        values = [self.args[ele.split(".")[-1]] for ele in selectData['where']]
                        whereCondAsDict = {}
                        for index,val in enumerate(values):
                            whereCondAsDict.update({selectData['where'][index] : val})
                        # print(""" whereCondAsDict """,whereCondAsDict)
                        self.selectResponse.append(self.connection.select(tables=selectData['from'],dataList=selectData['fields'],whereDict=whereCondAsDict,conditions=selectData['extension']))
                    else:
                        print(self.args)
                        # for key in self.args:
                            # print("{}\t\t\t{}".format(key,self.args[key]))
                        for element in selectData['fields']:
                            # print(indexVal,self.args[element])
                            self.selectResponse.append(self.args[element])
                print("selectResponse:",self.selectResponse)
            else:
                pass
            if(self.update):
                for element in self.update:
                    table = element['table']
                    setVar = self.processSetCondition(element['set'])
                    print("setVar",setVar)
                    whereCondAsDict = {}
                    for index,val in enumerate(values):
                        whereCondAsDict.update({selectData['where'][index] : val})
                    print("""-whereCondAsDict """,whereCondAsDict)
                    self.connection.update(tableName=table,setDict=setVar,whereDict=whereCondAsDict)
                print(self.update)
            #self.cursor.commit()
        else:
            print("Requires a 'case' condition ... Exitting")
            exit(0)
        print(self.selectResponse)

    def run(self,tableName):
    	self.tableName = tableName
    	if(tableName == ""):
    		print("break")
    	elif(tableName == ""):
    		print("break")
    	else:
    		print("break")

    def updatedAttendece(self):
        print('updatedAttendece')

    def updatedStudents(self):
        print("updatedStudents")


def test1():
    connection = sql.mysqlConnector(host='localhost',user='testuser',password='testpassword',database='rail_db')
    cursor = connection.setConnection()
    #mysqlConnection = connection.__getConnection__()
    process = analytics(connection,cursor,rail_id="RSK17CS036")
    process.generateAnalytics('login')
    connection.commitChanges()
    #connection.commitChanges()


if __name__ == "__main__":
    test1()
else:
    pass