#!/usr/bin/python3
import socket
import logging
import os
import sys
import database as db
import errors

_PORT_NUMBER = 49500


PATH = None
pathToExeFromCurDir = sys.argv[0]
current_directory = os.getcwd()
if(pathToExeFromCurDir.startswith("/")):
	PATH = pathToExeFromCurDir
elif(pathToExeFromCurDir.startswith(".")):
	PATH = current_directory + pathToExeFromCurDir[1:]
else:
	PATH = current_directory + "/" + pathToExeFromCurDir
PATH = PATH.rsplit("/",1)[0] + "/"

logging.basicConfig(
    filename=PATH+'socket.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

logging.debug("The path is:"+PATH)

logging.warning("SERVER STARTUP")
print("SERVER STARTUP")
logging.warning(f"The socket is starting up on port number:{_PORT_NUMBER}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.info(f"Successfully started a server:{sock}")
sock.bind(('', _PORT_NUMBER))
sock.listen(5)

try:
    while True:
        logging.debug("The server is in IDLE condition")
        clientSocket, address = sock.accept()
        data = clientSocket.recv(1024)
        if not data:
            break
        logging.info("Got data replying with the same")
        clientSocket.sendall(data)
        process = db.main(data.decode('utf-8'), 0) # decoding from bytes to utf-8
        process.setConnection()
        process.processRequest()
        process.generateAnalytics()
        process.closeConnection()
        # logging.info(f"clientSocket:{clientSocket}, address:{address}")
        # clientSocket.send(bytes("welcome to the server","utf-8"))
except KeyboardInterrupt:
    logging.info("KeyboardInterrupt")
    logging.warning("SERVER SHUTDOWN")
# except Exception as err:
#     errors.UserDefinedError(f"Uncaught error in input.py:{str(err.__class__)}:{str(err)}")
#     logging.warning("SERVER SHUTDOWN")