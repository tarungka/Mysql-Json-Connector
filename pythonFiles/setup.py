#!/usr/bin/python3
import mysqlConnector as sql
import json
import logging


logging.basicConfig(
        filename='railApplication.log',
        format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )


def main(jsonCnf):
	db = sql.mysqlConnector(option_files=".config/mysql.cnf")
	databases = (jsonCnf["databases"])
	allDatabases = databases.keys()
	for databaseName in allDatabases:
		try:
			db.use(databaseName)
			answer = input("Database %s is present, are you sure you want to drop it(Y/N)?" % (databaseName))
			if(answer == 'y' or answer == 'Y'):
				db.drop("database",databaseName)
				logging.info("Database " + databaseName + " was dropped.")
			else:
				logging.info("There already exists a database by the name " + databaseName + " please drop it.")
				return
		except:
			logging.info("No database by the name '" + databaseName + "',no need to drop.")
	for databaseName in allDatabases:
		print("Creating database %s ..." % (databaseName),end='')
		db.create("database",databaseName)
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
			print("Creating table %s ..." % (table),end='')
			db.create("table",table,dictionary=dictionary,primaryKey=primaryKey,foreignKeys=foreignKeys,indexAttributes=index)
			print("(success)")
			logging.info("Creating table %s ...(success)" % (table))


if __name__ == '__main__':
	logging.info("Start of setup.py")
	with open('.config/database.json') as configFile:
		logging.debug("Successfully opened the config file.")
		jsonCnf = json.load(configFile)
		main(jsonCnf)
	logging.info("End of setup.py")
else:
	print("This code does not support being imported as a module")
