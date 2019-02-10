import json
import hashlib
import jsonMysqlParser as parser

def main():
    parse = parser.jsonConfiguration("json/config_mysql.json")
    databases = list(parse.getDatabases())
    #tableDictionary = parse.getRelation()
    newtables = list(parse.getRelation().values())
    tables = []
    dictionary = {}
    count = 0
    for tableSet in newtables:
        for atable in tableSet:
            tables.append(atable)
            encrypt = hashlib.md5(atable.encode())
            dictionary.update({encrypt.hexdigest() : databases[count]})
        count = count + 1
    print(dictionary)
    jsonString = json.dumps(dictionary,indent=4)
    print(jsonString)
    parse.saveAs("json/testHashes.json",jsonString)

if __name__ == "__main__":
    main()
else:
    print("Does not yet support being imported as a module")