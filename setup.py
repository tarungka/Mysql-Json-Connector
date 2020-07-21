#!/usr/bin/python3
import mysqlConnector as sql
import json
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
PATH = PATH.rsplit("/", 1)[0] + "/"


logging.basicConfig(
    filename=PATH+'railApplication.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


def createDatabase(db, databases):
    allDatabases = databases.keys()
    for databaseName in allDatabases:
        try:
            db.use(databaseName)
            answer = input(f"Database '{databaseName}' is present, are you sure you want to drop it(Y/N)?")
            if(answer == 'y' or answer == 'Y'):
                db.drop("database", databaseName)
                logging.info("Database " + databaseName + " was dropped.")
                print("Database " + databaseName + " was dropped.")
            else:
                logging.info(f"There already exists a database by the name `{databaseName}` please drop it.")
                print(f"There already exists a database by the name `{databaseName}` please drop it.")
                exit(0)
        # Ok this gets buggy when its only "except:" or "except BaseException as e", Why?-- Is it because exit(0) raises an BaseException?
        except Exception as e:
            logging.info(f"No database by the name `{databaseName}`,no need to drop.{str(e)}")
    for databaseName in allDatabases:
        print("Creating database %s ..." % (databaseName), end='')
        db.create("database", databaseName)
        print("(success)")
        logging.info("Creating database %s ...(success)" % (databaseName))
        db.use(databaseName)
        tableObject = databases[databaseName]
        logging.debug(tableObject)
        allTables = tableObject["tables"].keys()
        logging.debug(allTables)
        for table in allTables:
            logging.debug("Inside the create table function")
            theTable = tableObject["tables"][table]
            dictionary = theTable["table_constrains"]
            index = theTable["index_constrains"]
            primaryKey = theTable["primary_key"]
            foreignKeys = theTable["foreign_key"]
            initial_data = theTable["initial_data"]
            print("Creating table '%s' ..." % (table), end='')
            db.create("table", table, dictionary=dictionary, primaryKey=primaryKey,foreignKeys=foreignKeys, indexAttributes=index)
            print("(success)")
            logging.info("Creating table %s ...(success)" % (table))
            if(initial_data):
                for eachData in initial_data:
                    print(f"Inserting intital data in table '{table}' ...",end='')
                    db.insert(table,eachData)
                    print("(success)")
                    logging.info(f"Inserting intital data in table '{table}' ...(success)")


def createProcedure(db, proc):
    if(proc):
        print("Creating procedures ...")
        logging.info("Creating procedures ...")
        # print(proc)
        for procedure in proc:
            print("Creating procedure {} ...(success)".format(procedure["procedure_name"]))
            db.procedure(procedure_name=procedure["procedure_name"],procedure_parameters=procedure["procedure_parameters"], procedures=procedure["procedures"])
            logging.info("Creating procedure {} ...(success)".format(procedure["procedure_name"]))


def createTrigger(db, triggers):
    if(triggers):
        print("Creating triggers ...")
        logging.info("Creating triggers ...")
        for trigger in triggers:
            db.trigger(trigger_name=trigger["trigger_name"], trigger_time=trigger["trigger_time"],database_name=trigger["database_name"], table_name=trigger["table_name"], queries=trigger["queries"])
            logging.info("Creating trigger on database {} trigger name {} ...(success)".format(trigger["database_name"], trigger["trigger_name"]))
            print("Creating trigger on database {} trigger name {} ...(success)".format(trigger["database_name"], trigger["trigger_name"]))


def createView(db, views):
    """ Creates a view """
    if(views):
        print("Creating views...")
        logging.info("Creating views...")
        for view in views:
            db.create("view",view["name"],view["query"])
            logging.info("Creating view '{}'".format(view["name"]))
            print("Creating view '{}'".format(view["name"]))



def insertInitialData(db, data):
    """
    To insert data to the database after creation of all
    the procedures and triggers
    """
    pass



def main(jsonCnf):
    """
    Creates a database with tables, procedures and triggers.
    """
    db = sql.mysqlConnector(option_files=PATH+".config/mysql.cnf")
    try:
        createDatabase(db, jsonCnf["databases"])
        createProcedure(db, jsonCnf["procedures"])
        createTrigger(db, jsonCnf["triggers"])
        createView(db, jsonCnf["views"])
        insertInitialData(db, jsonCnf["initial_data"])
    except KeyError:
        logging.critical(
            "The config file is either corrupted or not configured properly - MISSING KEY FIELDS")
    except Exception as e:
        logging.critical(
            "An error raised, could be an ERROR that breaks the program:"+(str(e)))
        pass  # Look at what error needs to be given
    else:
        db.commitChanges()


if __name__ == '__main__':
    logging.info("Start of setup.py")
    logging.debug("The path is:"+PATH+'.config/database.json')
    with open(PATH+'.config/database.json') as configFile:
        logging.debug("Successfully opened the config file.")
        jsonCnf = json.load(configFile)
        # sys.setrecursionlimit(15000)
        main(jsonCnf)
    logging.info("End of setup.py")
else:
    print("This code does not support being imported as a module")
