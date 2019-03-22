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
			#	THE FOLLOWING CODE IS A BIT BUGGY, WILL NEED TO FIX IT.
			#	REMOVED AS OF NOW, WILL ADD IT BACK AFTER REMOVING THE BUGS
			#	DATED 22 MAR 2019 21:17:23
			'''
			print("Setting index values for table %s ..." % table)
			allIndexes = tableObject["tables"][table]["index_constrains"]
			print(allIndexes)
			try:
				for index in allIndexes:
					print(index)
					print(query.indexQuery(table,index,index))
					cursor.execute(query.indexQuery(table,index,list(index)))
			except TypeError as error:
				print()
				print("TypeError:This table does not have any index value(s). ->",error)
			except IndexError:
				print(error)
				print("IndexError:This table does not have any index value(s). ->",error)
			'''
	logger.log("All databases and tables are created",True)
	#logger.log("Setting index values.",True)



if __name__ == '__main__':
	logger.log("Loading configuration File ...")
	with open('.config/database.json') as configFile:
		jsonCnf = json.load(configFile)
		main(jsonCnf)
else:
	print("This code does not support being imported as a module")
