import mysql.connector
from mysql.connector import errorcode



class analytics:
    def __init__(self):
        #Write code here to load the data
        self.connection = mysql.connector.connect(
            host = "localhost",
            user = "testuser",
            passwd = "testuser",
            database = "railDB"
        )
        self.cursor = self.connection.cursor()
        print("Constructor")
    def updatedAttendece(self):
        print('updatedAttendece')
        self.cursor.execute("SELECT * FROM  attendence")
        fetchedData = self.cursor.fetchall()
        #for data in fetchedData:
        #    if(data[4] != None):
        #        #print(data[1],data[4] - data[3])
        #        print              ("UPDATE attendence set time_spent='"+str(data[4] - data[3])+"' where time_in='"+str(data[3])+"' and rail_id ='"+str(data[0])+"';")
        #        self.cursor.execute("UPDATE attendence set time_spent='"+str(data[4] - data[3])+"' where time_in='"+str(data[3])+"' and rail_id ='"+str(data[0])+"';")
        dictionary = {}
        for data in fetchedData:
            if(data[0] in list(dictionary.keys())):
                if(data[4] != None):
                    #print(data,"update to",dictionary[data[0]])
                    print("UPDATE attendence SET time_since_last_login='"+dictionary[data[0]].strftime('%Y-%m-%d %H:%M:%S')+"' WHERE rail_id='"+data[0]+"' AND time_in='",str(data[3]),"';")
                    self.cursor.execute("UPDATE attendence SET time_since_last_login='"+dictionary[data[0]].strftime('%Y-%m-%d %H:%M:%S')+"' WHERE rail_id='"+data[0]+"' AND time_in='",str(data[3]),"';")
            dictionary.update({data[0] : data[3]})
        #print(dictionary)
        #print(len(dictionary.keys()))
        #print(data[1])
        self.connection.commit()
        #print("WORKING")
        #print(fetchedData[1][3])
        #print(fetchedData[1][4])
        #print(fetchedData[1][4] - fetchedData[1][3])
    def updatedStudents(self):
        print("updatedStudents")

if __name__ == '__main__':
    analytics = analytics()
    analytics.updatedAttendece()
else:
    print("This code does not support being imported as a module")