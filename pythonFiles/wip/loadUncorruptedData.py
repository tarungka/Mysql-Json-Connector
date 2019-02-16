import mysql.connector
import import_logger

logger = import_logger.logIt(__file__)

load = {
    "2019-02-15 17:30:39" :   "2019-02-15 08:00:00",
    "2019-02-15 14:50:29" :   "2019-02-15 08:00:00"
}


connection = mysql.connector.connect(
    host		=	"localhost",
    user		=	"testuser",
    passwd		=	"testpassword",
    database    =   "railDB"
)

cursor = connection.cursor()

keys = load.keys()

for key in keys:
    cursor.execute("SELECT * FROM attendence WHERE time_out = '%s'" % (key))
    fetchedData = cursor.fetchall()
    logger.log(("OLD DATA:"+str(fetchedData)))
    cursor.execute("UPDATE attendence SET time_in = '%s' WHERE time_out = '%s'" % (load[key],key))
    cursor.execute("SELECT * FROM attendence WHERE time_out = '%s'" % (key))
    fetchedData = cursor.fetchall()
    logger.log(("NEW DATA:"+str(fetchedData)))
connection.commit()