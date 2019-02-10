import json
import datetime
import constants
import query
import import_logger

logger =  import_logger.logIt(__file__)
data = constants.constData()
projectsTable = data._DICT_ALLTABLES_["PROJECTS_OF_RAIL_TABLE"]

def insert(dictionary,cursor):
	executeQuery = query.insertQuery(projectsTable,dictionary)
	logger.log(executeQuery)
	cursor.execute(executeQuery)

def read(cursor,returnType = "json"):
	executeQuery = query.selectQuery(data._READ_PROJECTS_LIST,projectsTable)
	cursor.execute(executeQuery)
	fetchedQuery = cursor.fetchall()
	print(fetchedQuery)
	if(returnType == "list"):
		return fetchedQuery
	elif(returnType == "json"):
		key = list(data._READ_PROJECTS_LIST)
		length = len(fetchedQuery)
		dictionaryList = {}
		for number in range(length):
			dictionary = {}
			#testing
			length = len(data._READ_PROJECTS_LIST)
			for index in range(length - 1):
				if(key[index + 1][0:4] == "date" or key[index + 1][0:4] == "time"):
					dictionary.update({data._READ_PROJECTS_LIST[index + 1] : fetchedQuery[number][index + 1].strftime('%d/%m/%Y')})
					continue
				dictionary.update({data._READ_PROJECTS_LIST[index + 1] : fetchedQuery[number][index + 1]})
			dictionaryList.update({fetchedQuery[number][0] : dictionary})
			print(dictionaryList)
		return json.dumps(dictionaryList)
	else:
		logger.log("The returnType is not supported",True)
		return None

def readEach(dictionary,cursor):
	#key = list(dictionary.keys())
	executeQuery = query.selectQuery("*",projectsTable,dictionary)
	logger.log(executeQuery)
	cursor.execute(executeQuery)
	fetchedQuery = cursor.fetchall()
	print(fetchedQuery)

def delete(dictionary,cursor):
	executeQuery = query.deleteQuery(projectsTable,dictionary)
	logger.log(executeQuery)
	cursor.execute(executeQuery)

#def update(setDictionary,whereDictionary,cursor):
#	print(query.updateQuery(projectsTable,setDictionary,whereDictionary))
def updateProjectDetails(whereDictionary,cursor):
	executeQuery = whereDictionary
	print(executeQuery)