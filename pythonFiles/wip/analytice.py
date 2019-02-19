import mysql.connector
from mysql.connector import errorcode



class analytics:
    def __init__(self):
        #Write code here to load the data
        self.connection = mysql.connector.connect(
            host = "localhost",
            user = "testuser",
            passwd = "testuser",
            database = "tdb"
        )
        self.cursor = self.connection.cursor()
        print("Constructor")
    def updatedAttendece(self):
        print('updatedAttendece')
        self.cursor.execute("SELECT * FROM  students_attendence")
        fetchedData = self.cursor.fetchall()
        for data in fetchedData:
            if(data[4] != None):
                #print(data[1],data[4] - data[3])
                print("UPDATE attendence set time_spent="+str(data[4] - data[3])," where time_in='"+str(data[3])+"' and rail_id ='"+str(data[0])+"';")
                self.cursor.execute("UPDATE attendence set time_spent=`"+str(data[4] - data[3]),"` where time_in ='"+str(data[3])+"' and rail_id ='"+str(data[0])+"';")
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