import mysql.connector
from mysql.connector import errorcode
import sys
import json
import query
import import_logger

logger =  import_logger.logIt(__file__)

class main:
	def __init__(self,jsonData):
		try:
			print("Trying to convert json data(of string datatype) to dictionary format ...",end='')
			self.jsonString = json.loads(str(jsonData))
			print("(success)")
		except:
			print("(failed)")
			print("Trying to assign data(of dict datatype) to dictionary format ...",end='')
			self.jsonString = jsonData			
			print("(success)")
		logger.log(str(self.jsonString))
		self.header = self.jsonString["HEADER"]
		self.requestType = self.header["REQUEST_TYPE"]
		self.data = self.jsonString["DATA"]
		self.fields = self.data["FIELDS"]
		self.where_clause = self.data["WHERE"]
		self.database = self.header["DATABASE"]
		self.table = self.header["TABLE_NAME"]
		self.footer = self.jsonString["FOOTER"]
		#print(self.footer)
		self.updateList = self.footer["UPDATE"]
		self.conditionList = self.footer["DEP"]
		#self.setConnection()
	def showData(self):
		print("jsonString",self.jsonString)
		print("request_type",self.requestType)
		print("header",self.header)
		print("data",self.data)
		print("footer",self.footer)
		print("database",self.database)
		print("table",self.table)
		print("update",self.updateList)
		print("condition",self.conditionList)

	def getDatabase(self):
		return self.database
	
	def getTable(self):
		return self.table
	
	def setConnection(self):
		self.mysqlConnection = mysql.connector.connect(
			host		=	"localhost",	#CREATE A CONFIG FILE FOR THIS AND GET DATA FROM IT.
			user		=	"testuser", 	#CREATE A CONFIG FILE FOR THIS AND GET DATA FROM IT.
			passwd		=	"testpassword", 	#CREATE A CONFIG FILE FOR THIS AND GET DATA FROM IT.
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
		#return finalQuery

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
		finalQuery = ("UPADTE %s SET " % (self.getTable()))
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
			finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
		finalQuery = finalQuery + ";"
		logger.log(finalQuery)
		self.cursor.execute(finalQuery)

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
			#print(length,key)
			finalQuery = finalQuery + key[0] + "=" + "'" + whereDict[key[0]] + "'"
			#print(finalQuery)
			for index in range((length - 1)):
				#print(index + 1)
				#print(key[0],whereDict[key[index +1]])
				#print(key[1],key[index +1])
				finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + whereDict[key[index + 1]] + "'"
			finalQuery = finalQuery + ";"
		logger.log(finalQuery)
		#self.cursor.execute
		self.cursor.execute(finalQuery)
		response = self.cursor.fetchall()
		return response

	def alterTable(self):
		return

	def processRequest(self):
		#print("START OF A PROCESS REQUEST ---------xxxxxxxxxx--------xxxxxxxxx--------xxxxxxxx--------")
		flag  = False
		#print("-----------------XXXXXXXXXXXXXXXXXXX--------------------")
		#print("Are there any condition lists? ...",end='')
		if(self.conditionList != None):
			#print("(YES)")
			for element in self.conditionList:
				#print(element)
				#print("-->INITIATING NEW OBJECT xxxxxxxxxxxxxxxxxxxxxxxx")
				process = main(element)
				process.setConnection()
				#process.showData()
				if process.processRequest():
					flag = True
				#print("-->DEATH NEW OBJECT xxxxxxxxxxxxxxxxxxxxxxxx")
			#print("-----------------XXXXXXXXXXXXXXXXXXX--------------------",self.conditionList,flag)
		if(self.conditionList == None or flag == True):
			'''
			KIMS THAT WHEN A SELECT IS USED IT RETURNS DATA AND CANNOT BE USED TO UPDATE ANOTHER TABLE.
			I NEED TO RESTRUCTURE IT TO BE ABLE TO RETURN AS WELL AS RUN AN UPDATE.
			'''
			#print("(NO)")
			#print("I'm inside")
			if(self.requestType == "insert"):
				self.insertData(self.fields)
				if(self.getTable == "attendence"):
					print("Need to update the current_students table")
			elif(self.requestType == "delete"):
				self.deleteData(self.fields,self.where_clause)
			elif(self.requestType == "update"):
				self.updateData(self.fields,self.where_clause)
			elif(self.requestType == "select"):
				#print("END OF A PROCESS REQUEST FROM SELECT---------xxxxxxxxxx--------xxxxxxxxx--------xxxxxxxx--------")
				return self.selectData(self.fields,self.where_clause)
			elif(self.requestType == "alter"):
				self.alterTable()
			#print("-----------------XXXXXXXXXXXXXXXXXXX--------------------")
			try:
				for anObject in self.updateList:
					print(anObject)
					process = main(anObject)
					#process.showData()
			except:
				logger.log("No data to update")
			self.mysqlConnection.commit()
		#print("END OF A PROCESS REQUEST ---------xxxxxxxxxx--------xxxxxxxxx--------xxxxxxxx--------")
	def analytics(self):
		print("a")

class analytics:
	def __init__(self):
		#Write code here to load the data
		print("Constructor")
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
