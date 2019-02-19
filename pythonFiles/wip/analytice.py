import mysql.connector
from mysql.connector import errorcode



class analytics:
    def __init__(self):
        #Write code here to load the data
        self.connection = mysql.connector.connect(
            host = "localhost",
            user = "testuser",
            passwd = "testpassword",
            database = "railDB"
        )
        self.cursor = self.connection.cursor()
        print("Constructor")
    def updatedAttendece(self):
        print('updatedAttendece')
        self.cursor.execute("SELECT * FROM  attendence")
        fetchedData = self.cursor.fetchall()
        print(fetchedData[1][3])
        print(fetchedData[1][4])
        print(fetchedData[1][4] - fetchedData[1][3])
    def updatedStudents(self):
        print("updatedStudents")

if __name__ == '__main__':
    analytics = analytics()
    analytics.updatedAttendece()
else:
    print("This code does not support being imported as a module")