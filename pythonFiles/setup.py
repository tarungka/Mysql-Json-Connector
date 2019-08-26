#!/usr/bin/python3
#import mysql.connector
#from mysql.connector import errorcode
#import query
#import logger
import mysqlConnector as sql
import json
import logging

#logger =  logger.logIt(__file__)

logging.basicConfig(
        filename='railApplication.log',
        format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )


def main(jsonCnf):
	#try:
	#	connection = mysql.connector.connect(
	#		host		=	jsonCnf["host"],
	#		user		=	jsonCnf["user"],
	#		passwd		=	jsonCnf["password"]
	#	)
	#	logging.debug("Connection to the database was successful")
	#except mysql.connector.Error as err:
	#	logging.critical("Connection failed to database ... EXITTING!"+str(err))
	#	exit(1)
	#cursor = connection.cursor()
	#DELETING DATABASE IF EXISTS
	db = sql.mysqlConnector(option_files=".config/mysql.cnf")
	databases = (jsonCnf["databases"])
	allDatabases = databases.keys()
	# print(databases)
	# exit(0)
	for databaseName in allDatabases:
		try:
			# print("are you working?")
			db.use(databaseName)
			# print("yes i am")
			answer = input("Database %s is present, are you sure you want to drop it(Y/N)?" % (databaseName))
			if(answer == 'y' or answer == 'Y'):
				db.drop("database",databaseName)
				logging.info("Database " + databaseName + " was dropped.")
			else:
				logging.info("There already exists a database by the name " + databaseName + " please drop it.")
				return
		except:
			logging.info("No database by the name '" + databaseName + "',no need to drop.")
	# exit(0)
	for databaseName in allDatabases:
		print("Creating database %s ..." % (databaseName),end='')
		db.create("database",databaseName)
		# cursor.execute(query.createQuery("database",databaseName))
		print("(success)")
		logging.info("Creating database %s ...(success)" % (databaseName))
		db.use(databaseName)
		# cursor.execute(query.useQuery(databaseName))
		tableObject = databases[databaseName]
		allTables = tableObject["tables"].keys()
		for table in allTables:
			dictionary = tableObject["tables"][table]["table_constrains"]
			index = tableObject["tables"][table]["index_constrains"]
			primaryKey = tableObject["tables"][table]["primary_key"]
			foreignKeys = tableObject["tables"][table]["foreign_key"]
			# print("->",type(index),type(index[0]))
			# exit(0)
			# print(table,dictionary,primaryKey,foreignKeys,index)
			print("Creating table %s ..." % (table),end='')
			db.create("table",table,dictionary=dictionary,primaryKey=primaryKey,foreignKeys=foreignKeys,indexAttributes=index)
			# cursor.execute(query.createQuery("table",table,dictionary))
			print("(success)")
			logging.info("Creating table %s ...(success)" % (table))
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
	#logger.log("All databases and tables are created",True)
	#logger.log("Setting index values.",True)



if __name__ == '__main__':
	logging.info("Start of setup.py")
	with open('.config/database.json') as configFile:
		logging.debug("Successfully opened the config file.")
		jsonCnf = json.load(configFile)
		main(jsonCnf)
	logging.info("End of setup.py")
else:
	print("This code does not support being imported as a module")
