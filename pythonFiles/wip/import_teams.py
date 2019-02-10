import json
import datetime
import constants
import query
import import_logger

logger =  import_logger.logIt(__file__)
data = constants.constData()
teamsTable = data._DICT_ALLTABLES_["TEAMS_OF_RAIL"]

def insert(dictionary,cursor):
    executeQuery = query.insertQuery(teamsTable,dictionary)
    logger.log(executeQuery,True)
    cursor.execute(executeQuery)

def delete(whereDictionary,cursor):
    executeQuery = query.deleteQuery(teamsTable,whereDictionary)
    logger.log(executeQuery,True)
    cursor.execute(executeQuery)

def readEach(dictionary,cursor):
    executeQuery = query.selectQuery(data._READ_TEAMS_LIST,teamsTable,dictionary)
    logger.log(executeQuery,True)
    cursor.execute(executeQuery)
    fetchedQuery = cursor.fetchall()
    print(fetchedQuery)


def read(cursor,returnType = "json"):
    executeQuery = query.selectQuery(data._READ_TEAMS_LIST,teamsTable)
    logger.log(executeQuery,True)
    cursor.execute(executeQuery)
    fetchedQuery = cursor.fetchall()
    #print(fetchedQuery)
    if(returnType == "list"):
    	return fetchedQuery
    elif(returnType == "json"):
    	key = list(data._READ_TEAMS_LIST)
    	length = len(fetchedQuery)
    	#dictionaryList = {}
    	for number in range(length):
    		dictionary = {}
    		#testing
    		length = len(data._READ_TEAMS_LIST)
    		for index in range(length):
    			if(key[index][0:4] == "date" or key[index][0:4] == "time"):
    				dictionary.update({data._READ_TEAMS_LIST[index] : fetchedQuery[number][index].strftime('%d/%m/%Y')})
    				continue
    			dictionary.update({data._READ_TEAMS_LIST[index] : fetchedQuery[number][index]})
    		#dictionaryList.update({fetchedQuery[number][0] : dictionary})
    		print(dictionary)
    	return json.dumps(dictionary)
    else:
    	logger.log("The returnType is not supported",True)
    	return None


def updateTeams(whereDictionary,cursor):
    print("a")
