import mysql.connector
from mysql.connector import errorcode
import query
import json
import import_logger
import jsonMysqlParser as parser
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
import sys
logger =  import_logger.logIt(__file__)

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
			#answer = input("Database %s is present, are you sure you want to drop it(Y/N)?" % (database))
			#if(answer == 'y' or answer == 'Y'):
			cursor.execute(query.dropQuery("database",database))
			#	logger.log(database + " was dropped.",True)
			#else:
			#	logger.log("Please change the name of the database in the config file and try again.",True)
			#	logger.log("Exitting",True)
			#	exit(0)
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
			cursor.execute(query.createQuery("table",table,dictionary))
	logger.log("All databases and tables are created",True)
	parse = parser.jsonConfiguration("json/config_mysql.json")
	allDatabases = parse.getDatabases()
	allTables = parse.getTables()
	#aesEncryptedTables = []
	#md5EncryptedTables = []
	jsonEncryption = {}
	print(sys.getsizeof(get_random_bytes(16)))
	encrypt = AES.new('b7061433023f48ecf254849b4df59745',AES.MODE_CBC,get_random_bytes(16))
	#dictionary = {}
	for table in allTables:
		print("Entering tables")
		print(table)
		print(encrypt.encrypt(table.ljust(16)))
		jsonEncryption.update({str(encrypt.encrypt(table.ljust(16))) : table})
		print(jsonEncryption)
		print("----------------------------")
		#print(encrypt.encrypt(get_random_bytes(16)))
		try: 
			print(encrypt.encrypt(table))
		except:
			print("Cannot print")
		#print(table.ljust(16))
	print(json.dumps(jsonEncryption))
	parse.saveAs("json/newSetupJson.json",json.dumps(jsonEncryption,indent=4))
	
	


if __name__ == '__main__':
	logger.log("Loading configuration File ...")
	with open('json/config_mysql.json') as configFile:
		jsonCnf = json.load(configFile)
		main(jsonCnf)
else:
	print("This code does not support being imported as a module")
