#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import sys
import json
import logger

logger =  logger.logIt(__file__)

class main:
	'''
	1)GET A BETTER NAME FOR THE CLASS
	2)WRITE BETTER DOCUMENTATION AS YOU GO
	3)PLAN BEFORE YOU WRITE THE ACTUAL CODE
	'''
	def __init__(self,jsonData):		#Constructor which decodes the incoming json data
		#print("The json data before convertion is:",type(jsonData))
		#print("The json data is:",jsonData)
		try:	#Checking if the input data is of string type
			print("Trying to convert json data(of string datatype) to dictionary format ...",end='')
			self.jsonString = json.loads(str(jsonData))
			print("(success)")
		except:	#Checking of the input data is of dict type
			print("(failed)")
			print("Trying to assign data(of dict datatype) to dictionary format ...",end='')
			self.jsonString = jsonData
			print("(success)")
		logger.log(str(self.jsonString))
		#print("The json data after convertion is",type(self.jsonString))
		
		self.header = self.jsonString["HEADER"]			#Gets the header 
		self.database = self.header["DATABASE"]			#database name within header
		self.table = self.header["TABLE_NAME"]			#table name name within header
		self.requestType = self.header["REQUEST_TYPE"]	#request type name within header
		
		self.data = self.jsonString["DATA"]				#Gets the data
		self.fields = self.data["FIELDS"]				#fields name within header
		self.setClause = self.data["SET"]				#setClause name within header
		self.whereClause = self.data["WHERE"]			#whereClause name within header
		
		self.footer = self.jsonString["FOOTER"]			#Gets the footer
		self.updateList = self.footer["UPDATE"]			#update name within header
		self.conditionList = self.footer["DEP"]			#dep name within header
		'''
		WRITE THE CODE HERE TO GET DATA ABOUT THE REQUEST AND THE COMMENT FROM THE FOOTER SECTION
		'''


	def showData(self):
		print("jsonString",self.jsonString)
		print("header			:",self.header)
		print("---database			:",self.database)
		print("---table name		:",self.table)
		print("---request type		:",self.requestType)
		print("data				:",self.data)
		print("---fields			:",self.fields)
		print("---set				:",self.setClause)
		print("---where				:",self.whereClause)
		print("footer			:",self.footer)
		print("---update			:",self.updateData)
		print("---dependency		:",self.conditionList)

	def getDatabase(self):
		return self.database
	
	def getTable(self):
		return self.table
	
	def setConnection(self):	#Establishes a connection between the script and the mysql database
		with open(".config/database.json") as cnfFile:
			data 	 = json.load(cnfFile)
			host 	 = data["host"]
			user 	 = data["user"]
			password = data["password"]
			self.mysqlConnection = mysql.connector.connect(
				host		=	host,		#CREATE A SEPERATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
				user		=	user, 		#CREATE A SEPERATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
				passwd		=	password, 	#CREATE A SEPERATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
				database	=	self.getDatabase()
			)
			self.cursor = self.mysqlConnection.cursor()
			return self.cursor
			#WRITE EXPECTIONS FOR THIS

	def insertData(self,insDict):
		logger.log("Generating CREATE query(%s) ..." % (self.getTable()))
		finalQuery = ("INSERT INTO %s(" % (self.getTable()))
		key = list(insDict.keys())
		value = list(insDict.values())
		length = len(key)
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
		logger.log(finalQuery,True)
		self.cursor.execute(finalQuery)

	def deleteData(self,delDict,whereDict):
		logger.log("Generating DELETE query(%s) ..." % (self.getTable()))
		finalQuery = ("DELETE FROM " + self.getTable() + " WHERE ")
		key = list(whereDict.keys())
		value = list(whereDict.values())
		length = len(key)
		finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
		for index in range(length - 1):
			finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + value[index + 1] + "'"
		finalQuery = finalQuery + ";"
		logger.log(finalQuery)
		self.cursor.execute(finalQuery)


	def updateData(self,setDict,whereDict):
		logger.log("Generating UPDATE query(%s) ..." % (self.getTable()))
		finalQuery = ("UPDATE %s SET " % (self.getTable()))
		key = list(setDict.keys())
		value = list(setDict.values())
		length = len(key)
		finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
		for index in range(length - 1):
			finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
		finalQuery = finalQuery + " WHERE "
		key = list(whereDict.keys())
		value = list(whereDict.values())
		length = len(key)
		finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
		for index in range(length - 1):
			if(value[index + 1].upper()	 == "NULL"):
				finalQuery = finalQuery + " AND " + key[index + 1] + " IS NULL"
				continue
			finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
		finalQuery = finalQuery + ";"
		logger.log(finalQuery)
		print("Query ready")
		self.cursor.execute(finalQuery)
		print("Query excuted")

	def selectData(self,dataList,whereDict = None):
		logger.log("Generating SELECT query(%s)" % (self.getTable))
		finalQuery = ("SELECT " + dataList[0])
		length = len(dataList)
		for index in range(length - 1):
			finalQuery = finalQuery + "," + dataList[index + 1]
		finalQuery = finalQuery + " FROM " + self.getTable()
		if(whereDict != None):
			finalQuery = finalQuery + " WHERE "
			key = list(whereDict.keys())
			length = len(key)
			finalQuery = finalQuery + key[0] + "=" + "'" + whereDict[key[0]] + "'"
			for index in range((length - 1)):
				finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + whereDict[key[index + 1]] + "'"
			finalQuery = finalQuery + ";"
		logger.log(finalQuery)
		self.cursor.execute(finalQuery)
		response = self.cursor.fetchall()
		return response

	def alterTable(self):
		print(" Alter table does not work")
		return

	def processRequest(self):
		flag  = False
		if(self.conditionList != None):
			for element in self.conditionList:
				subProcess = main(element)
				subProcess.setConnection()
				if subProcess.processRequest():
					flag = True
		if(self.conditionList == None or flag == True):
			'''
			KIMS THAT WHEN A SELECT IS USED IT RETURNS DATA AND CANNOT BE USED TO UPDATE ANOTHER TABLE.
			I NEED TO RESTRUCTURE IT TO BE ABLE TO RETURN AS WELL AS RUN AN UPDATE.
			'''
			if(self.requestType == "insert"):
				self.insertData(self.fields)
				#if(self.getTable == "attendence"):
				#	print("Need to update the current_students table")
			elif(self.requestType == "delete"):
				self.deleteData(self.fields,self.whereClause)
			elif(self.requestType == "update"):
				self.updateData(self.setClause,self.whereClause)
			elif(self.requestType == "select"):
				print(type(self.fields))
				return self.selectData(self.fields,self.whereClause)
			elif(self.requestType == "alter"):
				self.alterTable()
			try:
				for anObject in self.updateList:
					print("Start of a sub process.")
					print(anObject)
					subProcess = main(anObject)
					subProcess.setConnection()
					subProcess.showData()
					subProcess.processRequest()
					print("End of the sub process.")
			except TypeError:
				pass
			except BaseException as e:
				logger.log("Exception Raised:"+str(e),True)
				exit(0)
			self.mysqlConnection.commit()


	def analytics(self):
		print("a")

class analytics:
	def __init__(self,connection,cursor):
		#Write code here to load the data
		self.connection = connection
		self.cursor = cursor
		print("Constructor")
	def run(self,tableName):
		self.tableName = tableName
		if(tableName == ""):
			print("break")
		elif(tableName == ""):
			print("break")
		else:
			print("break")
	def updatedAttendece(self):
		print('updatedAttendece')
	def updatedStudents(self):
		print("updatedStudents")


if __name__ == '__main__':
	process = main(sys.argv[1])
	#process.showData()
	process.setConnection()
	process.processRequest()
else:
	print("This code does not support being imported as a module")


"""
python3 newdatabase.py '
{
	"HEADER":{
		"DATABASE":"railDB",
		"TABLE_NAME":"current_students",
		"REQUEST_TYPE":"insert"
	},
	"DATA":{
		"FIELDS": 
		{
			"rail_id": "RSK15EC053", 
			"student_name": "TARAKESHAVA C R ", 
			"gender": "M",
			"date_of_birth" : "1999-08-21",
			"associated_team" : "A",
			"usn": "1SK17CS002", 
			"branch": "CS", 
			"time_of_joining_rail": "2019-02-20 06:20:42", 
			"email": "ananth@gmail.com", 
			"phone_number": "9880233073"
		},
		"SET":null,
		"WHERE":null
	},
	"FOOTER" : {
		"DATA ABOUT THE REQUEST" : "just a test",
		"COMMENT" : "THIS IS A TEST",
		"DEP" : null,
		"UPDATE" : null
	}
}
'
python3 newdatabase.py '
{
	"HEADER":{
		"DATABASE":"railDB",
		"TABLE_NAME":"attendence",
		"REQUEST_TYPE":"insert"
	},
	"DATA":{
		"FIELDS": 
		{
			"rail_id": "RSK15EC053", 
			"purpose" : "TESTING",
			"time_in" : "2019-02-20 9:00:20",
			"current_team": "A"
		},
		"SET":null,
		"WHERE":null
	},
	"FOOTER" : {
		"DATA ABOUT THE REQUEST" : "just a test",
		"COMMENT" : "THIS IS A TEST",
		"DEP" : [
			{
				"HEADER":{
					"DATABASE":"railDB",
					"TABLE_NAME":"current_student",
					"REQUEST_TYPE":"select"
				},
				"DATA":{
					"FIELDS":{
						"rail_id": "RSK17CS002"
					},
					"SET":null,
					"WHERE":null
				},
				"FOOTER" : {
					"DATA ABOUT THE REQUEST" : "just a test",
					"COMMENT" : "THIS IS A TEST",
					"DEP" : null,
					"UPDATE" : null
				}
			}
		],
		"UPDATE" : [
			{
				"HEADER":{
					"DATABASE":"railDB",
					"TABLE_NAME":"attendence",
					"REQUEST_TYPE":"select"
				},
				"DATA":{
					"FIELDS": null,
					"SET":{
						"time_since_last_login" : "railDB.current_students.most_recent_login - railDB.attendence.time_in"
					},
					"WHERE":{
						"rail_id": "RSK17CS002"
					}
				},
				"FOOTER" : {
					"DATA ABOUT THE REQUEST" : "just a test",
					"COMMENT" : "THIS IS A TEST",
					"DEP" : null,
					"UPDATE" : null
				}
			},
			{
				"HEADER":{
					"DATABASE":"railDB",
					"TABLE_NAME":"current_student",
					"REQUEST_TYPE":"select"
				},
				"DATA":{
					"FIELDS": null,
					"SET":{
						"most_recent_login" : "2019-02-20 9:00:20"
					},
					"WHERE":{
						"rail_id": "RSK17CS002"
					}
				},
				"FOOTER" : {
					"DATA ABOUT THE REQUEST" : "just a test",
					"COMMENT" : "THIS IS A TEST",
					"DEP" : null,
					"UPDATE" : null
				}
			}
		]
	}
}
'

"""
