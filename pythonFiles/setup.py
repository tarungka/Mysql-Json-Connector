import __future__
import mysql.connector
from mysql.connector import errorcode
import query
import constants as const
import import_logger

logger =  import_logger.logIt(__file__)
data = const.constData()

def main():
	try:
		connection = mysql.connector.connect(
			host=const._host,
			user=const._user,
			passwd=const._pass,
		)
		logger.log(str(connection),True)		
		data = const.constData()
		cursor = connection.cursor()
		#DELETE THIS LINE JUST BEFORE PRODUCTION
		#cursor.execute("USE testdatabase;")
		try:
			cursor.execute("DROP DATABASE tdb;")
		except:
			print("tdb does not exits!")

		logger.log("Getting data for creation of the database")
		allDatabasesList = list(data._DICT_ALLDATABASES_.keys())
		#length = len(allDatabasesList)
		for alist in allDatabasesList:
			print(alist)
			cursor.execute(query.createQuery("database",data._DICT_ALLDATABASES_[alist]))
			cursor.execute(query.useQuery(data._DICT_ALLDATABASES_[alist]))
			#repectiveTable = 
			cursor.execute(query.createQuery("table",data._DICT_ALLTABLES_["STUDENT_DETAILS_TABLE"],data._DICT_STUDENTS_QUERY))
			cursor.execute(query.createQuery("table",data._DICT_ALLTABLES_["STUDENT_ATTENDANCE_TABLE"],data._DICT_STUDENTS_ATTENDENCE_QUERY))
			cursor.execute(query.createQuery("table",data._DICT_ALLTABLES_["PROJECTS_OF_RAIL_TABLE"],data._DICT_PROJECT_QUERY))
			cursor.execute(query.createQuery("table",data._DICT_ALLTABLES_["TEAMS_OF_RAIL"],data._DICT_TEAMS_QUERY))
			cursor.execute(query.createQuery("table",data._DICT_ALLTABLES_["COMPONENTS_TABLE"],data._DICT_COMPONENTS_QUERY))
			cursor.execute(query.createQuery("table",data._DICT_ALLTABLES_["ADMIN_DETAILS_TABLE"],data._DICT_ADMIN_QUERY))
		connection.commit()
		logger.log("Database and the tables have been created and the command are committed to the mysql database.")

	except mysql.connector.Error as err:
		logger.log("An error occured.")
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			logger.log("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			logger.log("Database does not exist")
		else:
			logger.log(err)
	else:
		cursor.close()
		connection.close()

if __name__ == '__main__':
	print("Enter the following details, the values in the bracket are default values. Just press enter if you want to retain them.")
	_buffer = input("Enter the host (%s): " % const._host)
	if(_buffer != ''):
		const._host = _buffer

	_buffer = input("Enter the user name (%s): " % const._user)
	if(_buffer != ''):
		const._user = _buffer
	
	_buffer = input("Enter the password (%s): " % const._pass)
	if(_buffer != ''):
		const._pass = _buffer
	
	_buffer = input("Enter the database (%s): " % const._database)
	if(_buffer != ''):
		const._database = _buffer

	main()
else:
	print("This code does not support being imported as a module")
