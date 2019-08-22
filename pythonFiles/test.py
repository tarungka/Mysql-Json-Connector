#!/usr/bin/python3
import mysqlConnector as sql
from re import finditer

class UserDefinedError(Exception):
    """Writing user defined errors"""
    def __init__(self,errorString):
        """Write documentation for this"""
        print(errorString)
        exit(0)

def add_back_ticks(tableNames,dataList):
    returnData = []
    #print("Incoming data",tableNames,dataList)
    for data in dataList:
        for tableName in tableNames:
            #print(tableName,data)
            val = [m.start() for m in finditer(tableName,data)]
            #print(val)
            #x,y = "",""
            #for eachVal in val:
            if(val and ("." in data)):
                if("=" in data):
                    returnData.append("=".join(add_back_ticks(tableNames,data.split("="))))
                    break
                else:
                    if(len(val) != 1): raise UserDefinedError("The list must contain only one element")
                    x = data[0:val[0]+len(tableName)+1]
                    y = "`" + (data)[val[0]+len(tableName)+1:] + "`"
                    returnData.append(x+y)
    #print("Incoming data-",returnData)
    return returnData



"""
if __name__ == "__main__":
    process = sql.mysqlConnector(host='localhost',user='testuser',password='testpassword',database='rail_db')
    process.showData()
    process.setConnection()
    data = process.select("cur_studs",["rail_id","student_name"])
    print(data)
else:
    exit(0)
"""

def run(string,a=10,b=20):
    print(a)
    print(b)
    print(string)


def x(**kwargs):
    print(kwargs)
    j = kwargs
    print(j)


if __name__ == "__main__":
    #run(string="what",b=10,a=500)
    #z = add_back_ticks(['attendence',"studs"],['attendence.time_in', 'attendence.time_out=attendence.time_in',"studs.groups","studs.groups=attendence.groups"])
    #print(z)
    x(a=10,b=20,c=30)