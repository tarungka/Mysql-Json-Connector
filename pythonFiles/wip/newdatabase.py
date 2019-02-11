import mysql.connector
from mysql.connector import errorcode
import sys
import json
import query
import import_logger

logger =  import_logger.logIt(__file__)

class main:
	def __init__(self,jsonData):
		#print("Init called.")
		self.jsonString = json.loads(jsonData)
		logger.log(self.jsonString)
		self.header = self.jsonString["HEADER"]
		self.requestType = self.header["REQUEST_TYPE"]
		self.data = self.jsonString["DATA"]
		self.fields = self.data["FIELDS"]
		self.where_clause = self.data["WHERE"]
		self.database = self.header["DATABASE"]
		self.table = self.header["TABLE_NAME"]
		self.footer = self.jsonString["FOOTER"]
		#self.setConnection()
	def showData(self):
		print("jsonString",self.jsonString)
		print("header",self.header)
		print("data",self.data)
		print("footer",self.footer)
		print("calss",self.__class__)
		print("database",self.database)
		print("table",self.table)
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
		return

	def updateData(self,setDict,whereDict):
		return

	def selectData(self,dataList,whereDict = None):
		return

	def alterTable(self):
		return

	def processRequest(self):
		if(self.requestType == "insert"):
			self.insertData(self.fields)
		elif(self.requestType == "delete"):
			self.deleteData(self.fields,self.where_clause)
		elif(self.requestType == "update"):
			self.updateData(self.fields,self.where_clause)
		elif(self.requestType == "select"):
			self.selectData(self.fields,self.where_clause)
		elif(self.requestType == "alter"):
			self.alterTable()
		self.mysqlConnection.commit()



if __name__ == '__main__':
	process = main(sys.argv[1])
	process.showData()
	process.setConnection()
	process.processRequest()
else:
	print("This code does not support being imported as a module")


"""
{
    "HEADER" : {
        "DATABASE" : "students",
        "TABLE_NAME" : "current_students",
        "REQUEST_TYPE" : "insert"
    },
    "DATA" : {
		"FIELDS" : {
			"rail_id"				:	"RSK17CS036",
			"student_name"			:	"TARUN GOPALKRISHNA A",
			"gender"				:	"M",
			"date_of_birth"			:	"1999-05-01",
			"time_of_joining_rail"	:	"2018-10-18 14:34:23",
			"phone_number"			:	"8296177426",
			"email"					:	"tarungopalkrishna@gmail.com",
			"associated_team"		:	"B",
			"projects_done"			:	"0",
			"branch"				:	"CS",
			"login_status"			:	"NO",
			"component_status"		:	"NO",
			"password"				:	"password",
			"usn"					:	"1SK17CS036",
			"time_in_rail"			:	"09:06:54",
			"current_highest_role"	:	"member"
		},
		"WHERE" : null
    },
    "FOOTER" : {
        "DATA ABOUT THE REQUEST" : "just a test",
        "COMMENT" : "THIS IS A TEST"
    }
}
"""