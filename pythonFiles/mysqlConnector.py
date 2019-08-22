#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import logging
from re import finditer

logging.basicConfig(
        filename='railApplication.log',
        format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )


class UserDefinedError(Exception):
    """Writing user defined errors"""
    def __init__(self,errorString):
        """Write documentation for this"""
        print(errorString)
        exit(0)

class InsufficientDataError(Exception):
    """Called when there is insufficient data passed to the class"""
    def __init__(self):
        self.showError()
        return
    
    def showError(self):
        print("Insifficient data passed")

class mysqlConnector():
    """
    This class is used to connect to the mysql database and peform basic mysql processes.  
    It supports only where condition as of now
    """
    def __init__(self,**kwargs):
        keys = kwargs.keys()
        try:
            if(set(["password","host","user","database"]).issubset(keys)):
                self.host = kwargs["host"]
                self.user = kwargs["user"]
                self.password = kwargs["password"]
                self.database = kwargs["database"]
            elif(set(["passwd","host","user","database"]).issubset(keys)):
                self.host = kwargs["host"]
                self.user = kwargs["user"]
                self.password = kwargs["passwd"]
                self.database = kwargs["database"]
            elif(set(["connection"]).issubset(keys)):
                logging.info("Trying to connect to the database")
                self.mysqlConnection = kwargs["connection"]
                self.cursor = self.mysqlConnection.cursor(dictionary=True)
                logging.info("Connection successful")
            else:
                raise InsufficientDataError()
        except InsufficientDataError:
            exit(0)
        except:
            print("Uncaught error in constructor of mysqlConnector class.")
            exit(0)

    def showData(self):
        print(self.host)
        print(self.user)
        print(self.password)
        print(self.database)

    def setConnection(self):
        """
        Check if there is already a connection present,this is needed because we can connect either throught an already
        existing connection or a new connection created now
        The cursor is returned.
        """
        try:
            logging.info("Trying to connect to the database")
            self.mysqlConnection = mysql.connector.connect(
            	host		=	self.host,
            	user		=	self.user,
            	passwd		=	self.password,
            	database	=	self.database
            )
            self.cursor = self.mysqlConnection.cursor(dictionary=True)
            logging.info("Connection successful")
            return self.cursor
        except mysql.connector.Error as err:
            logging.critical("Mysql connector error Error No:%4d:%s" % (err.errno,str(err.msg)))
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            	logging.critical("Access was denied.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
            	logging.critical("Database does not exist.")
            elif err.errno == errorcode.ER_BAD_FIELD_ERROR:
            	logging.critical("Invalid field.")
            elif err.errno == errorcode.ER_BAD_TABLE_ERROR:
            	logging.critical("Table does not exist.")
            else:
            	logging.critical(str(err.msg))
            print("Error while connecting to he database, check the logs!")
            exit(0)

    def __getConnection__(self):
        return self.mysqlConnection

    def add_back_ticks(self,tableNames,dataList):
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

    def insert(self,tableName,insDict):
        logging.info("Generating CREATE query(%s) ..." % (tableName))
        finalQuery = ("INSERT INTO %s(" % (tableName))
        key = list(insDict.keys())
        value = list(insDict.values())
        length = len(key)
        finalQuery = finalQuery + "`" + key[0] + "`"
        for index in range(length - 1):
            finalQuery = finalQuery + "," + "`" + key[index + 1] + "`"
        finalQuery = finalQuery + ") VALUES("
        finalQuery = finalQuery + "'" + str(value[0]) + "'"
        for index in range(length - 1):
            if(value[index + 1] == "null"): #THE BLOCK BELOW GENEREATES ",null"
                finalQuery = finalQuery + "," + str(value[index + 1])
                continue
            finalQuery = finalQuery + "," + "'" + str(value[index + 1]).replace("'",r"\'") + "'" #THE BLOCK BELOW GENEREATES ",'val'"
        finalQuery = finalQuery + ");"
        logging.debug(finalQuery)
        self.cursor.execute(finalQuery)

    def delete(self,tableName,delDict,whereDict):
        logging.info("Generating DELETE query(%s) ..." % (tableName))
        finalQuery = ("DELETE FROM " + tableName + " WHERE ")
        key = list(whereDict.keys())
        value = list(whereDict.values())
        length = len(key)
        finalQuery = finalQuery + key[0] + "=" + "'" + str(value[0]) + "'"
        for index in range(length - 1):
            finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + str(value[index + 1]) + "'"
        finalQuery = finalQuery + ";"
        logging.debug(finalQuery)
        self.cursor.execute(finalQuery)

    def update(self,tableName,setDict,whereDict):
        logging.info("Generating UPDATE query(%s) ..." % (tableName))
        finalQuery = ("UPDATE %s SET " % (tableName))
        key = list(setDict.keys())
        value = list(setDict.values())
        length = len(key)
        finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
        for index in range(length - 1):
            finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
        finalQuery = finalQuery + " WHERE "
        key = list(whereDict.keys())
        value = list(whereDict.values())
        length = len(key)
        finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
        for index in range(length - 1):
            if(value[index + 1].upper()	 == "NULL"):
                finalQuery = finalQuery + " AND " + key[index + 1] + " IS NULL"
                continue
            finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + value[index + 1] + "'"
        finalQuery = finalQuery + ";"
        logging.debug(finalQuery)
        print("Query ready")
        self.cursor.execute(finalQuery)
        print("Query excuted")

    #def select(self,tableName,dataList,whereDict = None):           
    def select(self,tables,dataList,whereDict = None,conditions = None):
        """
        PLEASE REMEMBER TO ADD BACK TICKS TO THE CONDTIONS IN CASE OF KEYWORDS OF MYSQL BEING USED AS A COLUMN HEADER
        """
        assert type(tables) is list and type(dataList) is list and ((type(whereDict) is dict) or (whereDict is None)) and ((type(conditions) is str) or (conditions is None))
        logging.info("Generating SELECT query(%s)" % (tables))
        finalQuery = ("SELECT ")
        length = len(dataList)
        finalQuery = finalQuery + ",".join(self.add_back_ticks(tables,dataList))
        finalQuery = finalQuery + " FROM " + ",".join(tables)
        if(whereDict != None):
            finalQuery = finalQuery + " WHERE "
            key = list(whereDict.keys())
            length = len(key)
            finalQuery = finalQuery + key[0] + "=" + "'" + whereDict[key[0]] + "'"
            for index in range((length - 1)):
                finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + whereDict[key[index + 1]] + "'"
        #    finalQuery = finalQuery + ";"
        #else:
        #    finalQuery = finalQuery +  ";"
        if(conditions):
            finalQuery = finalQuery + " " + conditions + ";"
        else:
            finalQuery = finalQuery +  ";"
        #print(finalQuery)
        logging.debug(finalQuery)
        self.cursor.execute(finalQuery)
        response = self.cursor.fetchall()
        logging.debug(response)
        return response


    def commitChanges(self):
        self.mysqlConnection.commit()

    def closeConnection_(self):
        self.mysqlConnection.closeConnection()
        pass



if __name__ == "__main__":
    print("No point running this!")
else:
    pass
