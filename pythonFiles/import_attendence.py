import json
import datetime
import import_student as importedStudent
import constants
import import_logger
import query

logger =  import_logger.logIt(__file__)
data = constants.constData()
attendenceTable = data._DICT_ALLTABLES_["STUDENT_ATTENDANCE_TABLE"]

def insert(dictionary,cursor):
	logger.log("Inside insert of attendence.",True)
	sendData = {}
	sendData.update({data._DICT_STUDENTS["RAIL_ID_HEADER"] : dictionary[data._DICT_STUDENTS["RAIL_ID_HEADER"]]})
	logger.log("sendData = ",True)
	print(sendData)
	studentData = importedStudent.readEach(sendData,cursor,"dict")
	dictionary.update({data._DICT_ATTENDENCE["NAME_HEADER"] : studentData[data._DICT_ATTENDENCE["NAME_HEADER"]]})
	if(studentData[data._DICT_STUDENTS["LOGIN_STATUS_HEADER"]] == "NO"):
		logger.log("Instering into attendence :" + dictionary[data._DICT_ATTENDENCE["RAIL_ID_HEADER"]])
		finalQuery = query.insertQuery(attendenceTable,dictionary)
		print("1->" + finalQuery)
		print("2->INSERT INTO %s(%s,%s,%s,%s,%s) VALUES('%s','%s','%s','%s','%s')" % (data._DICT_ALLTABLES_["STUDENT_ATTENDANCE_TABLE"],data._DICT_ATTENDENCE["NAME_HEADER"],data._DICT_ATTENDENCE["RAIL_ID_HEADER"],data._DICT_ATTENDENCE["TIME_IN_HEADER"],data._DICT_ATTENDENCE["CURRENT_TEAM_HEADER"],data._DICT_ATTENDENCE["PURPOSE_HEADER"],dictionary[data._DICT_ATTENDENCE["NAME_HEADER"]],dictionary[data._DICT_ATTENDENCE["RAIL_ID_HEADER"]],dictionary[data._DICT_ATTENDENCE["TIME_IN_HEADER"]],dictionary[data._DICT_ATTENDENCE["CURRENT_TEAM_HEADER"]],dictionary[data._DICT_ATTENDENCE["PURPOSE_HEADER"]]))
		number = input("Option 1 or 2?")
		if(number == 1):
			cursor.execute(finalQuery)
		elif(number == 2):
			cursor.execute("INSERT INTO %s(%s,%s,%s,%s,%s) VALUES('%s','%s','%s','%s','%s')" % (data._DICT_ALLTABLES_["STUDENT_ATTENDANCE_TABLE"],data._DICT_ATTENDENCE["NAME_HEADER"],data._DICT_ATTENDENCE["RAIL_ID_HEADER"],data._DICT_ATTENDENCE["TIME_IN_HEADER"],data._DICT_ATTENDENCE["CURRENT_TEAM_HEADER"],data._DICT_ATTENDENCE["PURPOSE_HEADER"],dictionary[data._DICT_ATTENDENCE["NAME_HEADER"]],dictionary[data._DICT_ATTENDENCE["RAIL_ID_HEADER"]],dictionary[data._DICT_ATTENDENCE["TIME_IN_HEADER"]],dictionary[data._DICT_ATTENDENCE["CURRENT_TEAM_HEADER"]],dictionary[data._DICT_ATTENDENCE["PURPOSE_HEADER"]]))
		else:
			print("Insert skipped")
			return
		importedStudent.updateLoginStatus("YES",dictionary[data._DICT_ATTENDENCE["RAIL_ID_HEADER"]],cursor)
		logger.log("Login Successful!",True)
		return
	elif(studentData[data._DICT_STUDENTS["LOGIN_STATUS_HEADER"]] == "YES"):
		logger.log("You are already Logged in!",True)
		return
	else:
		logger.log("The RAIL ID passed was not found in the database/or not registered.",True)

def read(cursor):
	query = "SELECT "
	length = len(data._READ_ATTENDENCE_LIST)
	query = query + data._READ_ATTENDENCE_LIST[0]
	for index in range(length - 1):
		query = query + "," + data._READ_ATTENDENCE_LIST[index + 1]
	query = query + " FROM " + data._DICT_ALLTABLES_["STUDENT_ATTENDANCE_TABLE"] + ";" 
	finalQuery = query.selectQuery(data._READ_ATTENDENCE_LIST,attendenceTable)
	print("1->",finalQuery)
	print("2->",query)
	number = input("Enter number:")
	if(number == 1):
		cursor.execute(finalQuery)
	elif (number == 2):
		cursor.execute(query)
	else:
		return
	fetchedQuery = cursor.fetchall()
	key = list(data._READ_ATTENDENCE_LIST)
	length = len(fetchedQuery)
	dictionaryList = {}
	for number in range(length):
		dictionary = {}
		length = len(data._READ_ATTENDENCE_LIST)
		for index in range(length - 1):
			if(key[index + 1][0:4] == "date" or key[index + 1][0:4] == "time"):
				dictionary.update({data._READ_ATTENDENCE_LIST[index + 1] : fetchedQuery[number][index + 1].strftime('%d/%m/%Y')})
				continue
			dictionary.update({data._READ_ATTENDENCE_LIST[index + 1] : fetchedQuery[number][index + 1]})
		dictionaryList.update({fetchedQuery[number][0] : dictionary})
	logger.log("Data read from mysqlDb->[" + query + "]")
	return json.dumps(dictionaryList)

def updateLogout(dictionary,cursor):
	query = ("UPDATE %s SET %s = '%s' where %s = '%s' AND %s IS null" % (data._DICT_ALLTABLES_["STUDENT_ATTENDANCE_TABLE"],data._DICT_ATTENDENCE["TIME_OUT_HEADER"],dictionary[data._DICT_ATTENDENCE["TIME_OUT_HEADER"]],data._DICT_ATTENDENCE["RAIL_ID_HEADER"],dictionary[data._DICT_ATTENDENCE["RAIL_ID_HEADER"]],data._DICT_ATTENDENCE["TIME_OUT_HEADER"]))
	finalQuery = query.updateQuery(attendenceTable,dictionary,dictionary)
	print("1->",finalQuery)
	print("2->",query)
	cursor.execute(query)
	logger.log("Updating table:" + query)
	importedStudent.updateLoginStatus("NO",dictionary[data._DICT_ATTENDENCE["RAIL_ID_HEADER"]],cursor)
