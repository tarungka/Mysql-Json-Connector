import json
import constants as const

constClass = const.constData()
constDict = constClass._DICT_STUDENTS

fileIn = open("json/allData.json","r")
fileOut = open("./allData.sh","w")
data = fileIn.read()
dictionary = json.loads(data)


#REGISTERED STUDENTS
#print(dictionary['students'])
newDictionary = dictionary['students']
key = dictionary['students'].keys()
#print(list(key))
#print(newDictionary["RSK17CS036"][0])
for akey in key:
    wrapperJson = {}
    newestDictionary = {}
    blah = newDictionary[akey]
    newestDictionary.update({constDict["RAIL_ID_HEADER"]        : blah["RAIL ID"]})
    newestDictionary.update({constDict["NAME_HEADER"]           : blah["STUDENT NAME"]})
    newestDictionary.update({constDict["GENDER_HEADER"]         : "M"})
    newestDictionary.update({constDict["USN_HEADER"]            : blah["USN"]})
    if(blah["BRANCH"] == "CSE"):
        newestDictionary.update({constDict["BRANCH_HEADER"]         : "CS"})
    else:
        newestDictionary.update({constDict["BRANCH_HEADER"]         : blah["BRANCH"]})
    newestDictionary.update({constDict["TIME_OF_JOINING_RAIL"]  : "2018-10-18 12:00:00"})
    newestDictionary.update({constDict["EMAIL_HEADER"]          : blah["EMAIL ADDRESS"]})
    newestDictionary.update({constDict["PHONE_NUMBER_HEADER"]   : blah["CONTACT NUMBER"]})
    #newestDictionary.update({"SET" : None})
    #newestDictionary.update({"WHERE" : None})
    #wrapperJson.update({"data" : newestDictionary})
    shellCommand = ("""python3 newdatabase.py '{"HEADER":{"DATABASE":"railDB","TABLE_NAME":"current_students","REQUEST_TYPE":"insert"},"DATA":{"FIELDS": """)
    shellCommand = shellCommand + str(json.dumps(newestDictionary)) + ""","SET":null,"WHERE":null},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'"""
    #print(shellCommand)
    #print(wrapperJson)
    #print(len(blah["EMAIL ADDRESS"]))
    fileOut.write(shellCommand + "\n")

#ATTENDENCE
#print(dictionary['students'])
newDictionary = dictionary['StudentsAttendence']
key = dictionary['StudentsAttendence'].keys()
#print(list(key))
#print(newDictionary["RSK17CS036"][0])
for akey in key:
    wrapperJson = {}
    newestDictionary = {}
    blah = newDictionary[akey]
    #print("newestDictionary[" + akey + "]['RAIL ID']")
    #print(blah["RAIL ID"])
    wrapperJson.update({"table_name" : "2"})
    wrapperJson.update({"request_type" : "login"})
    newestDictionary.update({"rail_id"          : blah["RAIL ID"]})
    newestDictionary.update({"student_name"     : blah["STUDENT NAME"]})
    aa = blah["DATE IN"] + " " + blah["TIME IN"]
    newestDictionary.update({"time_in"          : aa})
    bb = blah["DATE OUT"] + " " + blah["TIME OUT"]
    newestDictionary.update({"time_out"         : bb})
    newestDictionary.update({"purpose"          : blah["PROJECT"]})
    wrapperJson.update({"data" : newestDictionary})
    shellCommand = ("python3 database.py ")
    shellCommand = shellCommand + "'" + str(json.dumps(wrapperJson)) + "'"
    #print(shellCommand)
    print(wrapperJson)
    #print(len(blah["EMAIL ADDRESS"]))
    fileOut.write(shellCommand + "\n")

exit(0)

#COMPONENTS
#print(dictionary['students'])
newDictionary = dictionary['component']
key = dictionary['component'].keys()
#print(list(key))
#print(newDictionary["RSK17CS036"][0])
for akey in key:
    wrapperJson = {}
    newestDictionary = {}
    blah = newDictionary[akey]
    #print("newestDictionary[" + akey + "]['RAIL ID']")
    #print(blah["RAIL ID"])
    wrapperJson.update({"table_name" : "1"})
    wrapperJson.update({"request_type" : "insert"})
    newestDictionary.update({constDict["RAIL_ID_HEADER"]        : blah["RAIL ID"]})
    newestDictionary.update({constDict["NAME_HEADER"]           : blah["STUDENT NAME"]})
    newestDictionary.update({constDict["GENDER_HEADER"]         : "M"})
    newestDictionary.update({constDict["USN_HEADER"]            : blah["USN"]})
    if(blah["BRANCH"] == "CSE"):
        newestDictionary.update({constDict["BRANCH_HEADER"]         : "CS"})
    else:
        newestDictionary.update({constDict["BRANCH_HEADER"]         : blah["BRANCH"]})
    newestDictionary.update({constDict["TIME_OF_JOINING_RAIL"]  : "2018-10-18 12:00:00"})
    newestDictionary.update({constDict["EMAIL_HEADER"]          : blah["EMAIL ADDRESS"]})
    newestDictionary.update({constDict["PHONE_NUMBER_HEADER"]   : blah["CONTACT NUMBER"]})
    wrapperJson.update({"data" : newestDictionary})
    shellCommand = ("python3 database.py ")
    shellCommand = shellCommand + "'" + str(json.dumps(wrapperJson)) + "'"
    #print(shellCommand)
    #print(wrapperJson)
    print(len(blah["EMAIL ADDRESS"]))
    fileOut.write(shellCommand + "\n")


