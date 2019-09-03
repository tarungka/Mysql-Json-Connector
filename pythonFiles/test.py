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
    import analytics
    process = sql.mysqlConnector(host='127.0.0.1',port=25000,user='connector',password='Conn_Rail_Connector',database='rail_test_db')
    blah = analytics.analytics("connection",**{"team_hash":"ABBA234F","rail_id":"RSK17CS036"})
    blah.generateAnalytics("login")
else:
    #run(string="what",b=10,a=500)
    #z = add_back_ticks(['attendence',"studs"],['attendence.time_in', 'attendence.time_out=attendence.time_in',"studs.groups","studs.groups=attendence.groups"])
    #print(z)
    #x(a=10,b=20,c=30)
    process = sql.mysqlConnector(host='127.0.0.1',port=25000,user='testuser_all',password='testpassword',database='rail_db')
    # process.setConnection()
    dictionary = {
                        "usn": "CHAR(10) NOT NULL",
                        "team_login": "CHAR(8) NOT NULL",
                        "rail_id": "CHAR(10) NOT NULL",
                        "student_name": "VARCHAR(100) NOT NULL",
                        "gender": "CHAR(1) NOT NULL",
                        "date_of_birth": "DATE NOT NULL"
    }
    primary = "usn"
    foreign =   [
                    {
                        "constraint_name": "constraint_1",
                        "foreign_table": "cur_studs",
                        "child_attribute": [
                            "rail_id"
                        ],
                        "parent_attribute": [
                            "rail_id"
                        ]
                    },
                    {
                        "constraint_name": "constraint_2",
                        "foreign_table": "cur_teams",
                        "child_attribute": [
                            "team_login"
                        ],
                        "parent_attribute": [
                            "team_hash"
                        ]
                    }
                ]
    # index = [['student_name'],['date_of_birth'],['student_name','date_of_birth']]
    # ans = process.create("TABLE","testtable",dictionary=dictionary,primaryKey=primary,foreignKeys=foreign,index=index)
    # process.commitChanges()
    # print(ans)

