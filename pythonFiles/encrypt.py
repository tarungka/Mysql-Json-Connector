import hashlib  #Need to write software to hash table names and store in the json format
import json

def validate(string,ifHashed):
	if(ifHashed == True):
		with open('hashes.json') as configFile:
		    jsonEnc = json.load(configFile)
		    return jsonEnc[string]
	else:
		print("ifHashed has to be set to True.")
		exit(1)