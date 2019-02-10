import constants
import import_logger

logger =  import_logger.logIt(__file__)
dictQuery = constants.constData()

def insertQuery(tableName,dictionary):
	logger.log("Generating CREATE query(%s) ..." % (tableName))
	finalQuery = ("INSERT INTO %s(" % (tableName))
	key = list(dictionary.keys())
	value = list(dictionary.values())
	length = len(list(dictionary.keys()))
	finalQuery = finalQuery + key[0]
	for index in range(length - 1):
		finalQuery = finalQuery + "," + key[index + 1]
	finalQuery = finalQuery + ") VALUES("
	finalQuery = finalQuery + "'" + value[0] + "'"
	for index in range(length - 1):
		if(value[index + 1] == "null"): #THE BLOCK BELOW GENEREATES ",null"
			finalQuery = finalQuery + "," + value[index + 1]
			continue
		finalQuery = finalQuery + "," + "'" + value[index + 1] + "'" #THE BLOCK BELOW GENEREATES ",'val'"
	finalQuery = finalQuery + ");"
	logger.log(finalQuery)
	return finalQuery
	

def updateQuery(tableName,setDictionary,whereDictionary):
	logger.log("Generating UPDATE query(%s) ..." % (tableName))
	finalQuery = ("UPADTE %s SET " % (tableName))
	key = list(setDictionary.keys())
	value = list(setDictionary.values())
	length = len(key)
	finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
	for index in range(length - 1):
		finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
	finalQuery = finalQuery + " WHERE "
	key = list(whereDictionary.keys())
	value = list(whereDictionary.values())
	length = len(key)
	finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
	for index in range(length - 1):
		finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
	finalQuery = finalQuery + ";"
	logger.log(finalQuery)
	return finalQuery
	

def deleteQuery(tableName,whereDictionary):
	logger.log("Generating DELETE query(%s) ..." % (tableName))
	finalQuery = ("DELETE FROM " + tableName + " WHERE ")
	key = list(whereDictionary.keys())
	value = list(whereDictionary.values())
	length = len(key)
	finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
	for index in range(length - 1):
		finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + value[index + 1] + "'"
	finalQuery = finalQuery + ";"
	logger.log(finalQuery)
	return finalQuery
	

def createQuery(what,nameOfWhat,dictionary = None):
	whatUpper = what.upper()
	logger.log("Generating CREATE query(%s) ..." % (nameOfWhat))
	if(whatUpper == "TABLE"):
		if(dictionary ==  None):
			return	None
		logger.log("Generating CREATE query for table(%s) ..." % (nameOfWhat))
		finalQuery = ("CREATE "+ whatUpper + " " + nameOfWhat + "(")
		key = list(dictionary.keys())
		value = list(dictionary.values())
		length = len(key)
		finalQuery = (finalQuery + key[0] + " " + value[0])
		for index in range(length - 1):
			#print(key[index + 1].upper())
			if(key[index + 1].upper() == "PRIMARY KEY"):
				finalQuery = (finalQuery + "," + key[index + 1] +  " (" + value[index + 1] + ")")
				continue
			finalQuery = (finalQuery + "," + key[index + 1] +  " " + value[index + 1])
		finalQuery = finalQuery + ");"
		logger.log(finalQuery)
		return finalQuery
	elif(whatUpper == "DATABASE"):
		logger.log("Generating CREATE query for database(%s) ..." % (nameOfWhat))
		finalQuery = ("CREATE " + whatUpper + " " + nameOfWhat + ";")
		logger.log(finalQuery)
		return finalQuery
	else:
		logger.log("THIS FUNCITON CAN ONLY CREATE ONLY 'TALBE' AND 'DATABASE'",True)

def useQuery(databaseName):
	logger.log("Generating USE query(%s) ..." % (databaseName))
	finalQuery = ("USE " + databaseName + ";")
	logger.log(finalQuery)
	return (finalQuery)

def dropQuery(what,name):
	logger.log("Generating DROP query(%s) ..." % (name))
	finalQuery = ("DROP %s %s;" % (what.upper(),name))
	logger.log(finalQuery)
	return (finalQuery)

def selectQuery(selectList,tableName,whereList = None):
	logger.log("Generating SELECT query(%s)" % (tableName))
	finalQuery = ("SELECT " + selectList[0])
	length = len(selectList)
	for index in range(length - 1):
		finalQuery = finalQuery + "," + selectList[index + 1]
	finalQuery = finalQuery + " FROM " + tableName
	if(whereList != None):
		finalQuery = finalQuery + " WHERE "
		key = list(whereList.keys())
		length = len(key)
		print(length,key)
		finalQuery = finalQuery + key[0] + "=" + "'" + whereList[key[0]] + "'"
		print(finalQuery)
		for index in range((length - 1)):
			print(index + 1)
			print(key[0],whereList[key[index +1]])
			print(key[1],key[index +1])
			finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + whereList[key[index + 1]] + "'"
		finalQuery = finalQuery + ";"
	logger.log(finalQuery)
	return finalQuery
