#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import logging
from re import finditer
import os
import sys
import errors

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


class mysqlConnector():

    """
    This class is used to connect to the mysql database and perform basic mysql processes.
    It supports CREATE,USE,INSERT,UPDATE,DELETE,SELECT,DROP,PROCEDURE AND TRIGGER functionalities.
    It supports only WHERE condition as of now(ONLY ONE VALUE CAN BEW MATCHED)
    Check if you must use == or is for comparing the datatypes for assert in the functions
    """

    def __init__(self, **kwargs):
        """
        Takes an argument called "mysql_connection"(which must be set to true)
        and "connection" which holds the mysql.connector object to reuse an already
        existing connection or takes a dictionary of elements to create a new connection.
        """
        try:
            if(kwargs["mysql_connection"]):
                logging.info("Using an already existing connection.")
                self.mysqlConnection = kwargs["connection"]
                self.cursor = self.mysqlConnection.cursor(dictionary=True)
                logging.info("Connection successful")
        except KeyError:
            logging.info("Creating a new connection with arguments")
            logging.debug("The arguments are:"+str(kwargs))
            self.mysqlConnection = mysql.connector.connect(**kwargs)
            self.cursor = self.mysqlConnection.cursor(dictionary=True)
            logging.info("Connection successful")
        except mysql.connector.Error as err:
            logging.critical("Mysql connector error Error No:%4d:%s" %(err.errno, str(err.msg)))
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
        except Exception as e:
            logging.critical("Error in connecting to the database:"+str(e))
            errors.UserDefinedError("Error please check the logs!")

    def _getConnectionId(self):
        return self.mysqlConnection.connection_id

    def _getConnection(self):
        """
        Return the current connection
        """
        return self.mysqlConnection

    def _getCursor(self):
        """
        Return the current cursor
        """
        return self.cursor

    def _add_back_ticks(self, dataList):
        """
        Add backticks to the database name and the table name to avoid mysql query errors.
        """
        logging.warning("THIS METHOD IS NEW AND COULD BE BUGGY, CONTACT DEVELOPER IN CASE OF ERROR!")
        try:
            assert (type(dataList) is list)
            logging.debug("Input data is"+str(dataList))
            returnData = []
            for data in dataList:
                if("." in data and (data[-1] != "`" and data[0] != "`")): #This is still buggy
                    db,tbl = data.split(".")
                    returnData.append("`"+db+"`.`"+tbl+"`")
                else:
                    returnData.append("`"+data+"`")
            if((returnData == None) or (returnData == [])):
                logging.critical("Method FAILED TO PERFORM INTENDEND ACTION")
                raise errors.UserDefinedError("CRITICAL:mysqlConnector module failed!")
            else:
                logging.debug("Output data is"+str(returnData))
                return returnData
        except AssertionError as err:
            logging.critical("dataList must be of list type but is of type"+str(type(dataList)))
            errors.UserDefinedError("CRITICAL ERROR")
        except Exception as err:
            errors.UserDefinedError("Exception not handeled:"+str(err.__class__)+str(err))

    def convertToUsableData(self,dataList):
        assert type(dataList) is list
        usableList = []
        logging.debug("The input dataList is:"+str(dataList))
        for aResponse in dataList:
            usableDict = {}
            for key in aResponse:
                usableDict[key] = str(aResponse[key])
            usableList.append(usableDict)
        logging.debug("Usable data is:"+str(usableList))
        return usableList

    def executeQuery(self, query=None,raiseExternally=False):
        """
        Execute a query.
        Write the part for raiseExternally part
        ER_BAD_DB_ERROR is db missing
        """
        logging.debug("Calling executeQuery")
        # if(query and raiseExternally): Write code for this
        if(query):
            try:
                logging.debug("Connection id "+str(self._getConnectionId())+",the query is:"+query)
                self.cursor.execute(query)
            except mysql.connector.ProgrammingError as err:
                if err.errno == errorcode.ER_PARSE_ERROR:
                    errors.UserDefinedError("ERROR IN THE SYNTAX {}".format(str(err)))
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    raise errors.UnknownDatabaseError()
                else:
                    errors.NonCriticalError("MYSQL ERROR:{},{}".format(err,err.errno))
            except mysql.connector.Error as err:
                    errors.NonCriticalError("MYSQL CONNECTOR ERROR:{}".format(str(err)))
            except Exception as e:
                errors.UserDefinedError("Error not handeled!:{}:{}".format(str(e.__class__),str(e)))
        else:
            logging.debug("executeQuery called with no arguments")

    def show(self):
        self.executeQuery("SHOW DATABASES")
        response = self.cursor.fetchall()
        logging.debug(f"The show databases are {response}")
        databases = []
        for database in response:
            if(database['Database'] == 'information_schema'):
                continue
            databases.append(database['Database'])
        result = {}
        logging.debug(f"The databases are {databases}")
        for database in databases:
            tables = []
            self.use(database)
            self.executeQuery("SHOW TABLES")
            response = self.cursor.fetchall()
            for element in response:
                for table_name in element:
                    tables.append(element[table_name])
            result.update({ database : tables })
        return result

    def create(self, what, nameOfWhat, dictionary=None, primaryKey=None, foreignKeys=None, indexAttributes=None):
        """
        NOTE FOR DEVELOPER: MIGHT NEED TO MAKE IT KWARGS LATER OR SPLIT IT TO DIFFERENT FUNCTIONS
        Generates a CREATE query.
        Following are the datatypes of the parameters:
        VARIABLE                    DATATYPE
        what                        str
        nameOfWhat                  str
        dictionary                  dict
        primaryKey                  list or None
        foreignKeys                 list or None
        index                       list or None

        Usage:
        `what` can take only two values 'DATABASE' or 'TABLE'

        `nameOfWhat` is the name of the database or the table

        `dictionary` is a dict datatype with the key as the field name and the value as the mysql datatype
        Example:
        {
            "id":"CHAR(10) NOT NULL:",
            "name":"VARCHAR(70) NOT NULL",
            "phone_number":"CHAR(10) NOT NULL
        }

        `primarykey` is the name of the primary key
        Example: ["id","id2"]

        `foreignKeys` is a list of dicts of the following format:
        [
            {
                "constraint_name": "NAME OF CONSTRAINT",
                "foreign_table_name": "TABLE NAME",
                "parent_attribute": [
                    "PARENT TABLE ATTRIBUTE NAME"
                ],
                "child_attribute": [
                    "CHILD TABLE ATTRIBUTE NAME"
                ]
            },
            {
                "constraint_name": "NAME OF CONSTRAINT",
                "foreign_table_name": "TABLE NAME",
                "parent_attribute": [
                    "PARENT TABLE ATTRIBUTE NAME",
                    "PARENT TABLE ATTRIBUTE NAME"
                ],
                "child_attribute": [
                    "CHILD TABLE ATTRIBUTE NAME",
                    "CHILD TABLE ATTRIBUTE NAME"
                ]
            }

            `index` is a list of lists with index constraint:
            Example:[["id","phone_number"],["phone_number"]]
        """
        whatUpper = what.upper()
        logging.info("Generating CREATE query for %s(%s) ..." %
                     (whatUpper, nameOfWhat))
        if(whatUpper == "TABLE"):
            if(dictionary == None):
                logging.info(
                    "dictionary passed is empty(null) ... aborting create")
                return
            finalQuery = ("CREATE " + whatUpper + " `" + nameOfWhat + "`(")
            key = list(dictionary.keys())
            value = list(dictionary.values())
            length = len(key)
            finalQuery = (finalQuery + "`" + key[0] + "` " + value[0])
            for index in range(length - 1):
                finalQuery = (finalQuery + ",`" +
                              key[index + 1] + "` " + value[index + 1])
            if(primaryKey):
                finalQuery = finalQuery + ",PRIMARY KEY("
                for index, element in enumerate(primaryKey):
                    if(index == 0):
                        finalQuery = finalQuery + "`" + element + "`"
                        continue
                    finalQuery = finalQuery + "," + "`" + element + "`"
                finalQuery = finalQuery + ")"
            if(foreignKeys):
                for number, eachKey in enumerate(foreignKeys):
                    constraintName = eachKey['constraint_name']
                    foreignTable = eachKey['foreign_table_name']
                    parentAttrib = eachKey['parent_attribute']
                    childAttrib = eachKey['child_attribute']
                    finalQuery = finalQuery + ","
                    if(constraintName):
                        finalQuery = finalQuery + "CONSTRAINT `" + constraintName + "` "
                    finalQuery = finalQuery + "FOREIGN KEY ("
                    for index, element in enumerate(childAttrib):
                        if(index == 0):
                            finalQuery = finalQuery + "`" + element + "`"
                            continue
                        finalQuery = finalQuery + "," + "`" + element + "`"
                    finalQuery = finalQuery + ")"
                    finalQuery = finalQuery + \
                        " REFERENCES `" + foreignTable + "` ("
                    for index, element in enumerate(parentAttrib):
                        if(index == 0):
                            finalQuery = finalQuery + "`" + element + "`"
                            continue
                        finalQuery = finalQuery + "," + "`" + element + "`"
                    finalQuery = finalQuery + ") ON DELETE CASCADE"
            if(indexAttributes):
                for eachIndex in indexAttributes:
                    finalQuery = finalQuery + ",INDEX("
                    for index, element in enumerate(eachIndex):
                        if(index == 0):
                            finalQuery = finalQuery + "`" + element + "`"
                            continue
                        finalQuery = finalQuery + "," + "`" + element + "`"
                    finalQuery = finalQuery + ")"
            finalQuery = finalQuery + ");"
        elif(whatUpper == "DATABASE"):
            finalQuery = ("CREATE " + whatUpper + " `" + nameOfWhat + "`;")  # Change to call _add_back_ticks
        elif(whatUpper == "VIEW"):
            finalQuery = ("CREATE " + whatUpper + " " + nameOfWhat + " AS " + dictionary)
        else:
            logging.warning(
                "THIS FUNCTION CAN ONLY CREATE ONLY 'TABLE' AND 'DATABASE'")
        self.executeQuery(finalQuery)

    def describe(self, table_name):
        """
        Generates a DESCRIBE query.
        """
        logging.info("Creating DESCRIBE query({})".format(table_name))
        finalQuery = "DESCRIBE {};".format("".join(self._add_back_ticks([table_name])))
        self.executeQuery(finalQuery)
        response = self.cursor.fetchall()
        logging.debug("The response from DESCRIBE is:"+str(response))
        return response


    def use(self, databaseName):
        """
        Generates a USE query.
        """
        logging.info("Creating USE query({})".format(databaseName))
        finalQuery = "USE {};".format("".join(self._add_back_ticks([databaseName])))
        self.executeQuery(finalQuery)

    def insert(self, tableName, insDict):
        """
        Generates a INSERT query.

        `insDict` is a dict datatype with key as column name and value as the value to insert.
        """
        logging.info("Generating CREATE query(%s) ..." % (tableName))
        finalQuery = ("INSERT INTO `%s`(" % (tableName))
        key = list(insDict.keys())
        value = list(insDict.values())
        length = len(key)
        finalQuery = finalQuery + "`" + key[0] + "`"
        for index in range(length - 1):
            finalQuery = finalQuery + "," + "`" + key[index + 1] + "`"
        finalQuery = finalQuery + ") VALUES("
        finalQuery = finalQuery + "'" + str(value[0]) + "'"
        for index in range(length - 1):
            if(value[index + 1] == "null"):  # THE BLOCK BELOW GENERATES ",null"
                finalQuery = finalQuery + "," + str(value[index + 1])
                continue
            # THE BLOCK BELOW GENERATES ",'val'"
            finalQuery = finalQuery + "," + "'" + \
                str(value[index + 1]).replace("'", r"\'") + "'"
        finalQuery = finalQuery + ");"
        logging.debug(f"insert finalQuery {finalQuery}")
        self.executeQuery(finalQuery)

    def delete(self, tableName, whereDict):
        """
        Generates a DELETE query.

        `whereDict` is a dict datatype which with key as column name and value as the value of the rows to delete.
        """
        logging.info("Generating DELETE query(%s) ..." % (tableName))
        finalQuery = ("DELETE FROM " + tableName + " WHERE ")
        directQuery = whereDict.get("__QUERY__")
        if(directQuery):
            finalQuery = finalQuery + directQuery
        else:
            key = list(whereDict.keys())
            value = list(whereDict.values())
            length = len(key)
            finalQuery = finalQuery + key[0] + "=" + "'" + str(value[0]) + "'"
            for index in range(length - 1):
                finalQuery = finalQuery + " AND " + \
                    key[index + 1] + "=" + "'" + str(value[index + 1]) + "'"
        finalQuery = finalQuery + ";"
        self.executeQuery(finalQuery)

    def update(self, tableName, setDict, whereDict):
        """
        Generates a DELETE query.

        `setDict` is a dict datatype with key as column name and value as the new value to be set as.

        `whereDict` is a dict datatype with key as column name and value as the value of the rows to update.
        """
        logging.info("Generating UPDATE query(%s) ..." % (tableName))
        finalQuery = ("UPDATE `%s` SET " % (tableName))
        key = list(setDict.keys())
        value = list(setDict.values())
        length = len(key)
        try:
            finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
        except TypeError:
            if(value[0]):
                finalQuery = finalQuery + key[0] + "=" + "'" + str(value[0]) + "'"
        for index in range(length - 1):
            finalQuery = finalQuery + "," + \
                key[index + 1] + "=" + "'" + value[index + 1] + "'"
        finalQuery = finalQuery + " WHERE "
        key = list(whereDict.keys())
        value = list(whereDict.values())
        length = len(key)
        finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
        for index in range(length - 1):
            if(value[index + 1].upper() == "NULL"):
                finalQuery = finalQuery + " AND " + key[index + 1] + " IS NULL"
                continue
            finalQuery = finalQuery + " AND " + \
                key[index + 1] + "=" + "'" + value[index + 1] + "'"
        finalQuery = finalQuery + ";"
        self.executeQuery(finalQuery)

    def select(self, tables, dataList, whereDict=None, conditions=None,**kwargs):
        """
        Generates a SELECT query.

        PLEASE REMEMBER TO ADD BACK TICKS TO THE CONDITIONS IN CASE OF KEYWORDS OF MYSQL BEING USED AS A COLUMN HEADER

        `tables` is a list of table's

        `dataList` is the list of columns to be returned

        `whereDict` is a dict datatype which with key as column name and value as the value of the rows to delete.

        `conditions` is of string datatype used to put conditions which are not supported by this function.
        Example: "LIMIT 1" or "OFFSET 20"
        """
        assert type(tables) is list and type(dataList) is list and ((type(whereDict) is dict) or (
            whereDict is None)) and ((type(conditions) is str) or (conditions is None))
        logging.info("Generating SELECT query(%s)" % (tables))
        finalQuery = ("SELECT ")
        length = len(dataList)
        finalQuery = finalQuery + ",".join(self._add_back_ticks(dataList))
        finalQuery = finalQuery + " FROM " + ",".join(self._add_back_ticks(tables))
        if(whereDict != None):
            finalQuery = finalQuery + " WHERE "
            key = list(whereDict.keys())
            length = len(key)
            directQuery = whereDict.get("__QUERY__")
            if(directQuery):
                finalQuery = finalQuery + directQuery
            else:
                finalQuery = finalQuery + "".join(self._add_back_ticks([key[0]])) + \
                    "=" + "'" + whereDict[key[0]] + "'"
                for index in range((length - 1)):
                    finalQuery = finalQuery + " AND " + \
                        "".join(self._add_back_ticks([key[index + 1]])) + "=" + "'" + \
                        whereDict[key[index + 1]] + "'"
        if(conditions):
            finalQuery = finalQuery + " " + conditions + ";"
        else:
            finalQuery = finalQuery + ";"
        self.executeQuery(finalQuery)
        response = self.cursor.fetchall()
        logging.debug("The response from SELECT is:"+str(response))
        someVar = kwargs.pop("user_data",True)
        if(someVar):
            logging.info("Returning as user usable data")
            return self.convertToUsableData(response)
        else:
            logging.info("Not returning as user usable data")
            return response

    def procedure(self, procedure_name, procedure_parameters, procedures):
        """
        Generates a PROCEDURE query.

        `procedure_name` is the name of the procedure.

        `procedure_parameters` is a list of parametes passed to the procedure.

        `procedures` is a list of queries to be executed.

        Example:
        {
            "procedure_name": "update_login",
            "procedure_parameters": [
                "IN theId CHAR(10)",
                "IN time DATETIME"
            ],
            "procedures": "UPDATE some_table SET login=time WHERE id=theId;"
        }
        This is broken down and then sent.
        """
        logging.info("Generating PROCEDURE query(%s)" % (procedure_name))
        finalQuery = "CREATE PROCEDURE `" + procedure_name + "` ("
        if(procedure_parameters):
            for index, element in enumerate(procedure_parameters):
                if(index == 0):
                    finalQuery = finalQuery + element
                    continue
                finalQuery = finalQuery + "," + element
        finalQuery = finalQuery + ") BEGIN "
        for element in procedures:
            finalQuery = finalQuery + element
        finalQuery = finalQuery + "END"
        self.executeQuery(finalQuery)

    def trigger(self, trigger_name, trigger_time, database_name, table_name, queries):
        """
        Generates a TRIGGER query.

        `trigger_name` is the name of the trigger.

        `trigger_time` is the time the trigger is fired.

        `database_name` is the name of the database.

        `table_name` the name of the table the trigger is set on.

        `queries` are the list of queries to be executed.

        Example:
        {
            "trigger_name": "TRIGGER_NAME",
            "trigger_time": "BEFORE INSERT",
            "database_name": "DATABASE_NAME",
            "table_name": "TABLE_NAME",
            "queries": [
                "INSERT INTO someTable SET something = NEW.someOtherThing;"
            ]
        }
        This is broken down and then sent.
        """
        logging.info("Generating TRIGGER query(%s)" % (trigger_name))
        finalQuery = "CREATE TRIGGER `" + trigger_name + "` " + trigger_time + \
            " ON `" + database_name + "`.`" + table_name + "` FOR EACH ROW BEGIN "
        for aQuery in queries:
            finalQuery = finalQuery + aQuery
        finalQuery = finalQuery + "END"
        self.executeQuery(finalQuery)

    def drop(self, what, db_name):
        """
        As of now only supports dropping a database.
        """
        logging.info("Dropping {}({})".format(what, db_name))
        finalQuery = "DROP DATABASE {};".format("".join(self._add_back_ticks([db_name])))
        self.executeQuery(finalQuery)

    def commitChanges(self):
        """
        Commits the changes made!
        """
        logging.warning("COMMITTING CHANGES TO DATABASE.")
        self.mysqlConnection.commit()

    def rollbackChanges(self):
        """
        Rollback the transaction
        """
        logging.warning("ROLLING BACK THE CHANGES.")
        self.mysqlConnection.rollback()

    def closeConnection(self):
        """
        This is still under development as its giving me errors when using this, please do not use this method.
        """
        self.cursor.close()
        self.mysqlConnection.close()


if __name__ == "__main__":
    print("No point running this!")
else:
    pass
