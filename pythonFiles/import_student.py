import json
import datetime
import constants
import query
import import_logger

logger =  import_logger.logIt(__file__)
data = constants.constData()
studentsTable = data._DICT_ALLTABLES_["STUDENT_DETAILS_TABLE"]

def insert(dictionary,cursor):
	logger.log("Inserting into students ...")
	executeQuery = query.insertQuery(studentsTable,dictionary)
	cursor.execute(executeQuery)
	logger.log("Inserting into table:" + dictionary[data._DICT_STUDENTS["RAIL_ID_HEADER"]])

def delete(dictionary,cursor):
	logger.log("Deleting from students ...")
	executeQuery = (query.deleteQuery(studentsTable,dictionary))
	cursor.execute(executeQuery)
	logger.log("Deleting record->" + executeQuery)


def read(cursor,returnType = "json"):
	logger.log("Reading from students ...")
	query = "SELECT "
	length = len(data._READ_LIST)
	query = query + data._READ_LIST[0]
	for index in range(length - 1):
		query = query + "," + data._READ_LIST[index + 1]
	query = query + " FROM " + studentsTable + ";" 
	cursor.execute(query)
	logger.log("Reading->" + query)
	fetchedQuery = cursor.fetchall()
	if(returnType == "list"):
		return fetchedQuery
	elif(returnType == "json"):
		length = len(fetchedQuery)
		dictionaryList = {}
		for number in range(length):
			dictionary = {}
			length = len(data._READ_LIST)
			for index in range(length - 1):
				dictionary.update({data._READ_LIST[index + 1] : fetchedQuery[number][index + 1]})
			dictionaryList.update({fetchedQuery[number][0] : dictionary})
		return json.dumps(dictionaryList)
	else:
		logger.log("The returnType is not supported",True)
		return None

#THE FOLLOWING FUNCTION IS NOT DYNAMIC
def readEach(dictionary,cursor,returnType = "json"):
	logger.log("Reading a single row students ...")
	query = "SELECT "
	length = len(data._READ_EACH_LIST)
	query = query + data._READ_EACH_LIST[0]
	for index in range(length - 1):
		query = query + "," + data._READ_EACH_LIST[index + 1]
	query = query + " FROM " + studentsTable + " WHERE "
	key = list(dictionary.keys())
	length = len(key)
	query = query + key[0] + "=" + "'" + dictionary[key[0]] + "'"
	for index in range(length - 1):
		query = query + "," + key[index + 1] + "=" + "'" + dictionary[key[index + 1]] + "'"
	query = query + ";"
	cursor.execute(query)
	logger.log("readEach->" + query)
	fetchedQuery = cursor.fetchall()
	if(returnType == "list"):
		return fetchedQuery
	elif(returnType == "dict"):
		length = len(data._READ_EACH_LIST)
		key = list(data._READ_EACH_LIST)
		dictionaryList = {}
		dictionary = {}
		try:
			for index in range(length):
				print(key[index][0:4])
				if(key[index][0:4] == "date" or key[index][0:4] == "time"):
					if(fetchedQuery[0][index] != None):
						dictionary.update({key[index] : fetchedQuery[0][index].strftime("%d/%m/%Y")})
						continue
				if(fetchedQuery[0][index] != None):
					dictionary.update({key[index] : fetchedQuery[0][index]})
		except IndexError:
			print("index: " + index)
		return dictionary
	elif(returnType == "json"):
		length = len(data._READ_EACH_LIST)
		key = list(data._READ_EACH_LIST)
		dictionaryList = {}
		dictionary = {}
		for index in range(length - 1):
			if(key[index + 1][0:4] == "date" or key[index + 1][0:4] == "time"):
				dictionary.update({key[index + 1] : fetchedQuery[0][index + 1].strftime('%d/%m/%Y')})
				continue
			dictionary.update({key[index + 1] : fetchedQuery[0][index + 1]})
			dictionaryList.update({fetchedQuery[0][0] : dictionary})
		return json.dumps(dictionaryList)
	else:
		print("The returnType is not supported")
		return None

#
#NEED WRITE BETTER CODE FOR THE FOLLWING FUNCITONS
#

def update(updField,newValue,refField,fieldValue,cursor):
	logger.log("Updating students ...")
	executeQuery = ("UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (data._DICT_ALLTABLES_["STUDENT_DETAILS_TABLE"],updField,newValue,refField,fieldValue))
	cursor.execute(executeQuery)
	logger.log("Updating->" + executeQuery)

def updateLoginStatus(value,rail_id,cursor):
	logger.log("Updating login status in students ...")
	executeQuery = ("UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (data._DICT_ALLTABLES_["STUDENT_DETAILS_TABLE"],data._DICT_STUDENTS["LOGIN_STATUS_HEADER"],value,data._DICT_STUDENTS["RAIL_ID_HEADER"],rail_id))
	cursor.execute(executeQuery)
	logger.log("Updating->""UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (data._DICT_ALLTABLES_["STUDENT_DETAILS_TABLE"],data._DICT_STUDENTS["LOGIN_STATUS_HEADER"],value,data._DICT_STUDENTS["RAIL_ID_HEADER"],rail_id))
