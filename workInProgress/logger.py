import datetime
class logIt:
	fileName = None
	def __init__(self,scriptName):
		self.fileName = scriptName
	def log(self,string,boolean = False):
		file = open("./mysqlconnector.log","a")
		try:
			file.write(self.fileName + ":" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')) + ":" + string + "\n")
		except:
			print("string must be of type 'str' but is of type:",type(string))
		file.close()
		if(boolean ==  True):
			print(string)
