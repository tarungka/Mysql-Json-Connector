import mysql.connector
from mysql.connector import errorcode
import sys
import constants
import import_student as student
import import_attendence as attendence
import import_projects as projects
import import_teams as teams
import json
#import import_component as component
import import_logger

logger =  import_logger.logIt(__file__)

def main(jsonIn):
	try:
		connection = mysql.connector.connect(
			host		=	"none",
			user		=	"none",
			passwd		=	"none",
			database	=	"null"
		)
		#print(connection)
		cursor = connection.cursor()
		#decrypt = constants.constData()
		logger.log("Table number:" + jsonIn["table_name"] + ",Request type:" + jsonIn["request_type"])
		if(jsonIn["table_name"] == "1"):
			if(jsonIn["request_type"] == "insert"):
				data = jsonIn["data"]
				student.insert(data,cursor=cursor)
			elif(jsonIn["request_type"] == "delete"):
				data = jsonIn["data"]
				student.delete(data,cursor=cursor)
			elif(jsonIn["request_type"] == "read"):
				logger.log(student.read(cursor=cursor),True)					#REMOVE THIS PRINT STATEMENT
			elif(jsonIn["request_type"] == "readeach"):
				data = jsonIn["data"]
				logger.log(student.readEach(data,cursor=cursor),True)			#REMOVE THIS PRINT STATEMENT
			else:
				logger.log("ERROR: REQUEST IS NOT INSERT OR DELETE",True)
		elif(jsonIn["table_name"] == "2"):
			logger.log("table_2,wev",True)
			if(jsonIn["request_type"] == "login"):
				#print("request_type is login")
				data = jsonIn["data"]
				attendence.insert(data,cursor=cursor)
			elif(jsonIn["request_type"] == "logout"):
				#print("request_type is logout")
				data = jsonIn["data"]
				attendence.updateLogout(data,cursor=cursor)
			elif(jsonIn["request_type"] == "read"):
				logger.log(attendence.read(cursor=cursor),True)
			else:
				logger.log("ERROR: REQUEST IS NOT LOGIN,LOGOUT OR READ",True)
				return
		elif(jsonIn["table_name"] == "3"): #COMPONENETS TABLE
			logger.log("Table selected is:",True)
		elif(jsonIn["table_name"] == "4"): #ADMIN DETAILS TABLE
			logger.log("Table selected is:",True)
		elif(jsonIn["table_name"] == "5"): #PROJECTS TABLE
			if(jsonIn["request_type"] == "insert"):
				data = jsonIn["data"]
				projects.insert(data,cursor=cursor)
			elif(jsonIn["request_type"] == "read"):
				#data = jsonIn["data"]
				projects.read(cursor=cursor)
			elif(jsonIn["request_type"] == "readeach"):
				data = jsonIn["data"]
				projects.readEach(data,cursor=cursor)
			elif(jsonIn["request_type"] == "delete"):
				data = jsonIn["data"]
				projects.delete(data,cursor=cursor)
			elif(jsonIn["request_type"] == "update"):
				data = jsonIn["data"]
				projects.updateProjectDetails(data,cursor=cursor)
			else:
				logger.log("request_type is not supported(%s)" % jsonIn["request_type"],True)
		elif(jsonIn["table_name"] == "6"): #TEAMS TABLE
			if(jsonIn["request_type"] == "insert"):
				data = jsonIn["data"]
				teams.insert(data,cursor)
			elif(jsonIn["request_type"] == "read"):
				teams.read(cursor)
			elif(jsonIn["request_type"] == "readeach"):
				data = jsonIn["data"]
				teams.readEach(data,cursor)
			elif(jsonIn["request_type"] == "update"):
				data = jsonIn["data"]
				teams.updateTeams(data,cursor)
			elif(jsonIn["request_type"] == "delete"):
				data = jsonIn["data"]
				teams.delete(data,cursor)
			else:
				logger.log("request_type is not supported(%s)" % jsonIn["request_type"],True)
		else:
			logger.log("Table does not exist.",True)
		cursor.close()
		connection.commit()
	except mysql.connector.Error as err:
		logger.log(("An error occured. ERROR NO: %d" % (err.errno)),True)
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			logger.log("Access was denied.",True)
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			logger.log("Database does not exist",True)
		elif err.errno == errorcode.ER_BAD_FIELD_ERROR:
			logger.log(("Invalid field : %s in table '%s'" % (err.msg,jsonIn["table_name"])),True)
		elif err.errno == errorcode.ER_BAD_TABLE_ERROR:
			logger.log("Table does not exist",True)
		else:
			logger.log(str(err),True)
	else:
		cursor.close()
		connection.close()

if __name__ == '__main__':
	result = json.loads(sys.argv[1])
	main(result)
else:
	print("This code does not support being imported as a module")
