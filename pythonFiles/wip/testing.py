#!/usr/bin/python3
import json
import os
import newdatabase
import mysql.connector

cursor = None
mysqlConnection = None

def setConnection():	#Establishes a connection between the script and the mysql database
    global cursor
    global mysqlConnection
    with open(".config/database.json") as cnfFile:
    	data 	 = json.load(cnfFile)
    	host 	 = data["host"]
    	user 	 = data["user"]
    	password = data["password"]
    	mysqlConnection = mysql.connector.connect(
    		host		=	host,		#CREATE A SEPERATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
    		user		=	user, 		#CREATE A SEPERATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
    		passwd		=	password, 	#CREATE A SEPERATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
    		database	=	"rail_db"
    	)
    	cursor = mysqlConnection.cursor()
    	#return cursor
    	#WRITE EXPECTIONS FOR THIS

setConnection()
#print(cursor,mysqlConnection)
x = newdatabase.analytics(cursor,mysqlConnection)
x.showData()