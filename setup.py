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
PATH = PATH.rsplit("/",1)[0] + "/"


logging.basicConfig(
    filename=PATH+'railApplication.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


def createDatabase(db,databases):
    allDatabases = databases.keys()
    for databaseName in allDatabases:
        try:
            db.use(databaseName)
            answer = input(
                "Database %s is present, are you sure you want to drop it(Y/N)?" % (databaseName))
            if(answer == 'y' or answer == 'Y'):
                db.drop("database", databaseName)
                logging.info("Database " + databaseName + " was dropped.")
                print("Database " + databaseName + " was dropped.")
            else:
                logging.info("There already exists a database by the name " + databaseName + " please drop it.")
                print("There already exists a database by the name " + databaseName + " please drop it.")
                return
        except:
            logging.info("No database by the name '" +
                         databaseName + "',no need to drop.")
    for databaseName in allDatabases:
        print("Creating database %s ..." % (databaseName), end='')
        db.create("database", databaseName)
        print("(success)")
        logging.info("Creating database %s ...(success)" % (databaseName))
        db.use(databaseName)
        tableObject = databases[databaseName]
        allTables = tableObject["tables"].keys()
        for table in allTables:
            dictionary = tableObject["tables"][table]["table_constrains"]
            index = tableObject["tables"][table]["index_constrains"]
            primaryKey = tableObject["tables"][table]["primary_key"]
            foreignKeys = tableObject["tables"][table]["foreign_key"]
            print("Creating table %s ..." % (table), end='')
            db.create("table", table, dictionary=dictionary, primaryKey=primaryKey,
                      foreignKeys=foreignKeys, indexAttributes=index)
            print("(success)")
            logging.info("Creating table %s ...(success)" % (table))

def createProcedure(db,proc):
    if(proc):
        print("Creating procedures ...")
        logging.info("Creating procedures ...")
        for procedure in proc:
            db.procedure(procedure_name=procedure["procedure_name"],
                         procedure_parameters=procedure["procedure_parameters"], procedures=procedure["procedures"])
            print("Creating trigger {} ...(success)".format(
                procedure["procedure_name"]))
            logging.info("Creating trigger {} ...(success)".format(
                procedure["procedure_name"]))

def createTrigger(db,triggers):
    if(triggers):
        print("Creating triggers ...")
        logging.info("Creating triggers ...")
        for trigger in triggers:
            db.trigger(trigger_name=trigger["trigger_name"], trigger_time=trigger["trigger_time"],
                       database_name=trigger["database_name"], table_name=trigger["table_name"], queries=trigger["queries"])
            logging.info("Creating trigger on database {} trigger name {} ...(success)".format(
                trigger["database_name"], trigger["trigger_name"]))
            print("Creating trigger on database {} trigger name {} ...(success)".format(
                trigger["database_name"], trigger["trigger_name"]))

def createView(db,views):
    """ Unfinished """
    pass

def main(jsonCnf):
    """
    Creates a database with tables, procedures and triggers.
    """
    db = sql.mysqlConnector(option_files=PATH+".config/mysql.cnf")
    try:
        createDatabase(db,jsonCnf["databases"])
        createProcedure(db,jsonCnf["procedures"])
        createTrigger(db,jsonCnf["triggers"])
    except:
        pass    #Look at what error needs to be given
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
