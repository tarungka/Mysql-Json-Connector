#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import query
import json
import logger

logger =  logger.logIt(__file__)

def main(jsonCnf):
	try:
		connection = mysql.connector.connect(
			host		=	jsonCnf["host"],
			user		=	jsonCnf["user"],
			passwd		=	jsonCnf["password"]
		)
	except mysql.connector.Error as err:
		logger.log("Connection failed to database.",True)
		logger.log(err.msg)
		exit(1)
	cursor = connection.cursor()
	#DELETING DATABASE IF EXISTS
	databases = (jsonCnf["databases"])
	for database in databases:
		try:
			cursor.execute(query.useQuery(database))
			answer = input("Database %s is present, are you sure you want to drop it(Y/N)?" % (database))
			if(answer == 'y' or answer == 'Y'):
				cursor.execute(query.dropQuery("database",database))
				logger.log(database + " was dropped.",True)
			else:
				logger.log("Please change the name of the database in the config file and try again.",True)
				logger.log("Exitting",True)
				exit(0)
		except:
			logger.log(database + " does not exist,no need to drop")
	allDatabases = databases.keys()
	for database in allDatabases:
		print("Creating database %s ..." % (database),end='')
		cursor.execute(query.createQuery("database",database))
		print("(success)")
		cursor.execute(query.useQuery(database))
		tableObject = databases[database]
		allTables = tableObject["tables"].keys()
		for table in allTables:
			dictionary = tableObject["tables"][table]["table_constrains"]
			print("Creating table %s ..." % (table),end='')
			cursor.execute(query.createQuery("table",table,dictionary))
			print("(success)")
	logger.log("All databases and tables are created",True)
	logger.log("Setting index values.",True)



if __name__ == '__main__':
	logger.log("Loading configuration File ...")
	with open('.config/database.json') as configFile:
		jsonCnf = json.load(configFile)
		main(jsonCnf)
else:
	print("This code does not support being imported as a module")
