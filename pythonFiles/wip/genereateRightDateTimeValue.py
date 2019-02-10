import datetime
import json

fileIn = open("./lmao.sh","r")
fileOut = open("./lmao_new.sh","w")

#print(data)

number = 1

for line in fileIn:
    #print(number)
    data = fileIn.readline()
    #print(data)
    newData = data[21:-2]
    if(newData != None):
        jsonData = json.loads(newData)
        garbageData = jsonData["data"]
        #print(jsonData["data"])
        #print(garbageData["time_in"][0:9])
        date = garbageData["time_in"][0:2]
        month = garbageData["time_in"][3:4]
        year = garbageData["time_in"][5:9]
        print(date,month,year)
        number = number + 1
#print(number)
#"dictionary" = json.loads(data)


