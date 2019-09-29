#!/usr/bin/python3
import socket
import logging
import os
import sys
import database as db       #This has a logging config
import errors
import json

#
#
#
_PORT_NUMBER = 49500
_BUFFER_SIZE = 2048
_MAX_CONNECT = 5        #Maximum number of connections
#
#
#

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

######################
# The following config is not taken as 'database' is imported before and has a config.
# If you want it to go to 'socket.log' then import 'database' after the below config.
######################
logging.basicConfig(
    filename=PATH+'socket.log',
    format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


logging.warning("SERVER STARTUP")
logging.debug("The path is:"+PATH)
print("SERVER STARTUP")
logging.warning(f"The socket is starting up on port number:{_PORT_NUMBER}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.info(f"Successfully started a server:{sock}")
sock.bind(('', _PORT_NUMBER))
sock.listen(_MAX_CONNECT)

########
# Look at presistent connections
########
process = db.main()
process.setConnection()




try:
    while True:
        logging.debug("The server is in IDLE condition")
        clientSocket, address = sock.accept()
        # print(f"{clientSocket}:{address}")
        logging.info(f"Got a request from {address},the clientSocket is {clientSocket}")
        data = clientSocket.recv(_BUFFER_SIZE)
        if(len(data) == _BUFFER_SIZE):
            logging.warning("The data size and the buffer size is the same, data could have been lost!")
            reply = {}
            reply.update({"reply_code":300})
            reply.update({"error":f"Data width is too big, current only {_BUFFER_SIZE} wide data is supported."})
            clientSocket.sendall(bytes(json.dumps(reply),"utf-8"))
            continue
        else:
            logging.debug(f"The data size is:{len(data)}")
        if not data:
            break
        logging.info("Got data replying with the same")
        logging.debug("The data is:"+data.decode('utf-8'))
        process.input(data.decode('utf-8'), 0)  #decoding from bytes to utf-8
        response = process.processRequest()
        logging.debug("The response is:"+str(response))
        reply = {}
        reply.update({"reply_code":200})
        reply.update({"data":str(response)}) #In the next version convert this into a pickle
        clientSocket.sendall(bytes(json.dumps(reply),"utf-8"))
        process.generateAnalytics()
except KeyboardInterrupt:
    logging.info("KeyboardInterrupt")
    logging.warning("SERVER SHUTDOWN")
    process.closeConnection()
    sock.close()
    print("SERVER SHUTDOWN")
# except Exception as err:
#     errors.UserDefinedError(f"Uncaught error in input.py:{str(err.__class__)}:{str(err)}")
#     logging.warning("SERVER SHUTDOWN")