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

    def __init__(self, errorString):
        """Write documentation for this"""
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
        logging.info(errorMessage)
        print(errorMessage)


class mysqlConnector():
    """
    This class is used to connect to the mysql database and perform basic mysql processes.
    It supports CREATE,USE,INSERT,UPDATE,DELETE,SELECT,DROP,PROCEDURE AND TRIGGER functionalities.
    It supports only WHERE condition as of now(ONLY ONE VALUE CAN BEW MATCHED)
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
            logging.debug("The arguments are", kwargs)
            self.mysqlConnection = mysql.connector.connect(**kwargs)
            self.cursor = self.mysqlConnection.cursor(dictionary=True)
            logging.info("Connection successful")
        except mysql.connector.Error as err:
            logging.critical("Mysql connector error Error No:%4d:%s" %
                             (err.errno, str(err.msg)))
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
            UserDefinedError("Error please check the logs!")

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

    def _add_back_ticks(self, tableNames, dataList):
        """
        Add backticks to the database name and the table name to avoid mysql query errors.
        """
        returnData = []
        for data in dataList:
            for tableName in tableNames:
                val = [m.start() for m in finditer(tableName, data)]
                if(val and ("." in data)):
                    if("=" in data):
                        returnData.append(
                            "=".join(self._add_back_ticks(tableNames, data.split("="))))
                        break
                    else:
                        if(len(val) != 1):
                            raise UserDefinedError(
                                "The list must contain only one element")
                        x = data[0:val[0]+len(tableName)+1]
                        y = "`" + (data)[val[0]+len(tableName)+1:] + "`"
                        returnData.append(x+y)
        return returnData

    def executeQuery(self, query=None):
        """
        Execute a query.
        """
        if(query):
            try:
                logging.debug(query)
                self.cursor.execute(query)
            except mysql.connector.ProgrammingError as err:
                NonCriticalError("MYSQL ERROR:{}".format(err))
            except:
                UserDefinedError("Error not handeled!")
        else:
            logging.debug("executeQuery called with no arguments")

    def create(self, what, nameOfWhat, dictionary=None, primaryKey=None, foreignKeys=None, indexAttributes=None):
        """
        Generates a CREATE query.
        Following are the datatypes of the parameters:
        VARIABLE                    DATATYPE
        what                        str
        nameOfWhat                  str
        dictionary                  dict
        primaryKey                  str or None
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
        Example: "id"

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
            Example:[["id","phone_number"],["phone_numbe"]]
        """
        whatUpper = what.upper()
        logging.info("Generating CREATE query for %s(%s) ..." %
                     (whatUpper, nameOfWhat))
        if(whatUpper == "TABLE"):
            if(dictionary == None):
                logging.info(
                    "dictionary passed is empty(null) ... aborting create")
                return
            finalQuery = ("CREATE " + whatUpper + " " + nameOfWhat + "(")
            key = list(dictionary.keys())
            value = list(dictionary.values())
            length = len(key)
            finalQuery = (finalQuery + "`" + key[0] + "` " + value[0])
            for index in range(length - 1):
                finalQuery = (finalQuery + ",`" +
                              key[index + 1] + "` " + value[index + 1])
            if(primaryKey):
                finalQuery = finalQuery + ",PRIMARY KEY(" + primaryKey + ")"
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
                    finalQuery = finalQuery + ")"
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
            # logging.debug(finalQuery)
        elif(whatUpper == "DATABASE"):
            finalQuery = ("CREATE " + whatUpper + " `" + nameOfWhat + "`;")
            # logging.debug(finalQuery)
        else:
            logging.warning(
                "THIS FUNCTION CAN ONLY CREATE ONLY 'TABLE' AND 'DATABASE'")
        self.executeQuery(finalQuery)

    def use(self, databaseName):
        """
        Generates a USE query.
        """
        logging.info("Creating USE query({})".format(databaseName))
        finalQuery = "USE {};".format(databaseName)
        self.executeQuery(finalQuery)
        # logging.debug(finalQuery)

    def insert(self, tableName, insDict):
        """
        Generates a INSERT query.

        `insDict` is a dict datatype with key as column name and value as the value to insert.
        """
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
            if(value[index + 1] == "null"):  # THE BLOCK BELOW GENERATES ",null"
                finalQuery = finalQuery + "," + str(value[index + 1])
                continue
            # THE BLOCK BELOW GENERATES ",'val'"
            finalQuery = finalQuery + "," + "'" + \
                str(value[index + 1]).replace("'", r"\'") + "'"
        finalQuery = finalQuery + ");"
        # logging.debug(finalQuery)
        self.executeQuery(finalQuery)

    def delete(self, tableName, whereDict):
        """
        Generates a DELETE query.

        `whereDict` is a dict datatype which with key as column name and value as the value of the rows to delete.
        """
        logging.info("Generating DELETE query(%s) ..." % (tableName))
        finalQuery = ("DELETE FROM " + tableName + " WHERE ")
        key = list(whereDict.keys())
        value = list(whereDict.values())
        length = len(key)
        finalQuery = finalQuery + key[0] + "=" + "'" + str(value[0]) + "'"
        for index in range(length - 1):
            finalQuery = finalQuery + " AND " + \
                key[index + 1] + "=" + "'" + str(value[index + 1]) + "'"
        finalQuery = finalQuery + ";"
        # logging.debug(finalQuery)
        self.executeQuery(finalQuery)

    def update(self, tableName, setDict, whereDict):
        """
        Generates a DELETE query.

        `setDict` is a dict datatype with key as column name and value as the new value to be set as.

        `whereDict` is a dict datatype with key as column name and value as the value of the rows to update.
        """
        logging.info("Generating UPDATE query(%s) ..." % (tableName))
        finalQuery = ("UPDATE %s SET " % (tableName))
        key = list(setDict.keys())
        value = list(setDict.values())
        length = len(key)
        finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
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
        # logging.debug(finalQuery)
        self.executeQuery(finalQuery)

    def select(self, tables, dataList, whereDict=None, conditions=None):
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
        finalQuery = finalQuery + \
            ",".join(self._add_back_ticks(tables, dataList))
        finalQuery = finalQuery + " FROM " + ",".join(tables)
        if(whereDict != None):
            finalQuery = finalQuery + " WHERE "
            key = list(whereDict.keys())
            length = len(key)
            finalQuery = finalQuery + key[0] + \
                "=" + "'" + whereDict[key[0]] + "'"
            for index in range((length - 1)):
                finalQuery = finalQuery + " AND " + \
                    key[index + 1] + "=" + "'" + \
                    whereDict[key[index + 1]] + "'"
        if(conditions):
            finalQuery = finalQuery + " " + conditions + ";"
        else:
            finalQuery = finalQuery + ";"
        # logging.debug(finalQuery)
        self.executeQuery(finalQuery)
        response = self.cursor.fetchall()
        logging.debug("The response from SELECT is:", response)
        return response

    def procedure(self, procedure_name, procedure_parameters, procedures):
        """
        Generates a PROCEDURE query.

        `procedure_name` is the name of the procedure.

        `procedure_parameters` is a list of parametes passed to the procedure.

        `procedures` is a string of queries to be executed.

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
        # logging.debug(finalQuery)
        self.executeQuery(finalQuery)

    def drop(self, what, db_name):
        """
        As of now only supports dropping a database.
        """
        logging.info("Dropping {}({})".format(what, db_name))
        finalQuery = "DROP DATABASE {}".format(db_name)
        self.executeQuery(finalQuery)
        # logging.debug("DROP DATABASE {}".format(db_name))

    def commitChanges(self):
        """
        Commits the changes made!
        """
        self.mysqlConnection.commit()

    def closeConnection_(self):
        """
        This is still under development as its giving me errors when using this, please do not use this method.
        """
        self.mysqlConnection.closeConnection()


if __name__ == "__main__":
    print("No point running this!")
else:
    pass
