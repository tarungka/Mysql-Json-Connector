#!/usr/bin/python3
import json
import os
import datetime

mode = "register"
message = """\t\t\tWELCOME TO RAIL REGISTRAION\nStuents can register as groups of 2 or 4."""

currentDatabase = list(json.load(open(".config/database.json"))["databases"].keys())[0]


class register:
    def __init__(self):
        global currentDatabase
        print(message)
        print("\t\t\tTEAM REGISTRATION")
        self.numberOfStudents = int(input("Enter the number of students(either 2 or 4)  :"))
        self.teamName =                  input("Enter team name(given by sir/admin)          :")
        self.projectName =               input("Name of the project                          :")
        self.current_db = currentDatabase

    def validateUSN(self,usn):
        no    = usn[0]
        #clg   = usn[1:3]
        year  = usn[3:5]
        #branch= usn[5:7]
        id    = usn[7:10]
        if(no.isdigit()):
            if(year.isdigit()):
                if(id.isdigit()):
                    pass
                else:
                    return False
            else:
                return False
        else:
            return False
        return True

    def generateRailId(self,usn):
        try:
            assert (self.validateUSN(usn)),"INVALID USN!"
            rail_id = 'R' + usn[-9:]
            return str(rail_id)
        except AssertionError as e:
            print("Error:",str(e))
            changeMode()

    def getStudentInformation(self,currentUsn):
        print("Enter the details of",currentUsn)
        name        =   input("Enter the student name   :")
        usn         =   currentUsn
        print("Usn                      :"+usn)
        print("Rail id                  :"+self.generateRailId(usn))
        gender      =   input("Enter your gender        :")
        dob         =   input("Enter your date of birth :")
        phNumber    =   input("Enter your phone number  :")
        email       =   input("Enter your email         :")
        team        =   self.team["team_name"]
        print("Team                     :"+team)
        branch      =   input("Enter your branch        :")
        role        =   input("Enter your role          :")
        studentDict = {}
        studentDict.update({"student_name"          :name})
        studentDict.update({"usn"                   :usn})
        studentDict.update({"rail_id"               :self.generateRailId(usn)})
        studentDict.update({"gender"                :gender})
        studentDict.update({"date_of_birth"         :dob})
        studentDict.update({"phone_number"          :phNumber})
        studentDict.update({"email"                 :email})
        studentDict.update({"associated_team"       :team})
        studentDict.update({"branch"                :branch})
        studentDict.update({"current_highest_role"  :role})
        return studentDict

    def registerStudents(self):
        self.students = []
        for student in self.team["team_members"]:
            self.students.append(self.getStudentInformation(student))
    
    def registerTeams(self):
        teamMembers = []
        if(self.numberOfStudents == 2):
            teamMembers.append(input("Enter the first students usn                 :"))
            teamMembers.append(input("Enter the second students usn                :"))
        elif(self.numberOfStudents == 4):
            teamMembers.append(input("Enter the first students usn                 :"))
            teamMembers.append(input("Enter the second students usn                :"))
            teamMembers.append(input("Enter the third students usn                 :"))
            teamMembers.append(input("Enter the fourth students usn                :"))
        else:
            print(" Error..!")
            exit(0)
        self.team = {}
        self.team.update({"team_name"            : self.teamName})
        self.team.update({"number_of_members"    : self.numberOfStudents})
        self.team.update({"associated_projects"  : self.projectName})
        self.team.update({"team_members"         : teamMembers})


    def registerProjects(self):
        print("\t\t\tPROJECT REGISTRATION")
        print("Project name                   :"+self.projectName)
        print("Team name                      :"+self.teamName)
        projectDescription  = input("Enter the project description  :")
        print("Number of members              :"+str(self.numberOfStudents))
        mentor              = input("Enter the mentor name          :")
        teamLead            = input("Enter the team lead rsn        :")
        ideaBy              = input("Idea by                        :")
        typeOfProject       = input("Enter the type of project      :")
        expectedDuration    = input("Enter the expected duration    :")
        priority            = input("Enter the project priority     :")
        status              = input("Enter the project status       :")
        technologyStack     = input("Enter the technology stack     :")
        self.project = {}
        self.project.update({"project_name"         : self.projectName})
        self.project.update({"associated_team"      : self.teamName})
        self.project.update({"project_description"  : projectDescription})
        self.project.update({"number_of_members"    : self.numberOfStudents})
        self.project.update({"mentor"               : mentor})
        self.project.update({"team_lead"            : teamLead})
        self.project.update({"idea_by"              : ideaBy})
        self.project.update({"type_of_project"      : typeOfProject})
        self.project.update({"expected_duration"    : expectedDuration})
        self.project.update({"status"               : status})
        self.project.update({"priority"             : priority})
        self.project.update({"technology_stack"     : technologyStack})

    def generateArgumentForStudent(self,inputDict):
        header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "cur_studs","REQUEST_TYPE" : "insert"},'
        firstHalf = '"DATA":{"FIELDS":'
        secondHalf = json.dumps(inputDict)
        thirdHalf = ',"SET" : null,"WHERE" : null},'
        footer = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'
        return (header + firstHalf + secondHalf + thirdHalf + footer)

    def generateArgumentForTeam(self,inputDict):
        header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "cur_teams","REQUEST_TYPE" : "insert"},'
        firstHalf = '"DATA":{"FIELDS":'
        secondHalf = json.dumps(inputDict)
        thirdHalf = ',"SET" : null,"WHERE" : null},'
        footer = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'
        return (header + firstHalf + secondHalf + thirdHalf + footer)

    def generateArgumentForProject(self,inputDict):
        header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "cur_projs","REQUEST_TYPE" : "insert"},'
        firstHalf = '"DATA":{"FIELDS":'
        secondHalf = json.dumps(inputDict)
        thirdHalf = ',"SET" : null,"WHERE" : null},'
        footer = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'
        return (header + firstHalf + secondHalf + thirdHalf + footer)

    def updateDatabase(self):
        for student in self.students:
            print(student)
        print(self.team)
        print(self.project)
        for student in self.students:
            studentArgument = self.generateArgumentForStudent(student)
            os.system("./database.py '" + studentArgument + "'")
        teamArgument    = self.generateArgumentForTeam(self.team)
        projectArgument = self.generateArgumentForProject(self.project)
        os.system("./database.py '" + teamArgument + "'")
        os.system("./database.py '" + projectArgument + "'")

class attendence:
    def __init__(self):
        global currentDatabase
        print("\t\t\tATTENDENCE")
        self.railId =               input("Enter RAIL ID                                :")
        self.action =               input("Login or Logout?                             :")
        if(self.action == 'login'):
            self.team =                 input("Enter team name(given by sir/admin)          :")
            self.reason =               input("Reason for attending rail                    :")
        self.convertToData()
        self.current_db = currentDatabase

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def convertToData(self):
        self.data = {}
        self.data.update({"rail_id"         : self.railId})
        if(self.action == "login"):
            self.data.update({"time_in"         : self.getCurrentTime()})
            self.data.update({"current_team"    : self.team})
            self.data.update({"purpose"         : self.reason})
        elif(self.action == "logout"):
            self.data.update({"time_out"        : self.getCurrentTime()})

    def generateArgumentForAttendence(self,inputDict):
        if(self.action == "login"):
            header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "attendence","REQUEST_TYPE" : "insert"},'
            firstHalf = '"DATA":{"FIELDS":'
            secondHalf = json.dumps(inputDict)
            thirdHalf = ',"SET" : null,"WHERE" : null},'
            footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "login","COMMENT" : "THIS IS A TEST","DEP" :'
            dep = '[{"HEADER":{"DATABASE":"rail_db","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id"],"SET":null,"WHERE":{"rail_id" : "' + self.railId + '","login_status":"NO"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
            footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"rail_db","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"login_status":"YES"},"WHERE":{"rail_id":"' + self.railId +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
            return (header + firstHalf + secondHalf + thirdHalf + footer_1 + dep + footer_3)
        elif(self.action == "logout"):
            header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "attendence","REQUEST_TYPE" : "update"},'
            firstHalf = '"DATA":{"FIELDS":null'
            thirdHalf = ',"SET" : {"time_out": "' + self.getCurrentTime() + '"},"WHERE" : {"rail_id" : "' + self.railId + '","time_out":"NULL"}},'
            footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "logout","COMMENT" : "THIS IS A TEST","DEP" :'
            dep = '[{"HEADER":{"DATABASE":"rail_db","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id","login_status"],"SET":null,"WHERE":{"rail_id" : "' + self.railId + '","login_status":"YES"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
            footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"rail_db","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"login_status":"NO"},"WHERE":{"rail_id":"' + self.railId +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "Just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
            return (header + firstHalf + thirdHalf + footer_1 + dep + footer_3)
        else:
            print("Something went wrong")

    def updateDatabase(self):
        attendenceArgument = self.generateArgumentForAttendence(self.data)
        #print(attendenceArgument)
        os.system("./database.py '" + attendenceArgument + "'")
        

class component:
    def __init__(self):
        global currentDatabase
        print("\t\t\tCOMPONENT")
        self.numberOfComponents= int(input("Number of components                        :"))
        self.requestType       =     input("Request/Return?                             :").upper()
        self.issuedTo           =    input("Enter your rail_id                          :")
        self.componentId = []
        for index in range(self.numberOfComponents):
            self.componentId.append(input("Enter the component id of component number %d:" % (index+1)))
        if(self.requestType == "REQUEST"):
            self.associatedTeam     =    input("Enter your associated team                  :")
        self.checkCompId()
        self.convertToData()
        self.current_db = currentDatabase

    def checkCompId(self):
        localComp = []
        for aComponent in self.componentId:
            if(not(aComponent.startswith("RL-"))):
                localComp.append("RL-" + aComponent)
            else:
                localComp.append(aComponent)
        self.componentId = localComp
    
    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def convertToData(self):
        self.data = []
        if(self.requestType == "REQUEST"):
            for aComponent in self.componentId:
                localDict = {}
                localDict.update({"component_id":aComponent})
                localDict.update({"issued_to":self.issuedTo})
                localDict.update({"associated_team":self.associatedTeam})
                self.data.append(localDict)
        elif(self.requestType == "RETURN"):
            for aComponent in self.componentId:
                localDict = {}
                localDict.update({"component_id":aComponent})
                localDict.update({"issued_to":self.issuedTo})
                #localDict.update({"associated_team":self.associatedTeam})
                localDict.update({"time_of_return": None})
                self.data.append(localDict)


    def generateArgumentForComponent(self,data):
        localList = []
        if(self.requestType == "REQUEST"):
            for aData in data:
                print(aData)
                header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "iss_compnts","REQUEST_TYPE" : "insert"},'
                firstHalf = '"DATA":{"FIELDS":'
                secondHalf = json.dumps(aData)
                thirdHalf = ',"SET" : null,"WHERE" : null},'
                footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "req_comp","COMMENT" : "THIS IS A TEST","DEP" :'
                dep = '[{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id"],"SET":null,"WHERE":{"rail_id" : "' + self.issuedTo + '","login_status":"YES"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
                footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"rail_db","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"component_status":"YES"},"WHERE":{"rail_id":"' + self.issuedTo +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
                localList.append((header + firstHalf + secondHalf + thirdHalf + footer_1 + dep + footer_3))
        elif(self.requestType == "RETURN"):
            for aData in data:
                print(aData)
                header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "iss_compnts","REQUEST_TYPE" : "update"},'
                firstHalf = '"DATA":{"FIELDS": null'
                thirdHalf = ',"SET" : {"time_of_return" : "' + self.getCurrentTime() + '"},"WHERE" : ' + json.dumps(aData) + '},'
                footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "ret_comp","COMMENT" : "THIS IS A TEST","DEP" :'
                dep = '[{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id"],"SET":null,"WHERE":{"rail_id" : "' + self.issuedTo + '","login_status":"YES"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
                footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"rail_db","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"component_status":"YES"},"WHERE":{"rail_id":"' + self.issuedTo +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
                localList.append((header + firstHalf + thirdHalf + footer_1 + dep + footer_3))
        return localList

    def updateDatabase(self):
        componentArguments = self.generateArgumentForComponent(self.data)
        for aData in componentArguments:
            os.system("./database.py '" + aData + "'")

    def showData(self):
        print("numberOfComponents   :",self.numberOfComponents)
        print("request/return       :",self.requestType)
        for index in range(self.numberOfComponents):
            print(("component no %d       :") % (index+1),self.componentId[index])
        #print("numberOfComponents:",self.numberOfComponents)
        #print("numberOfComponents:",self.numberOfComponents)



def changeMode():
    global mode
    print("The availabe modes are:")
    print("register")
    print("attendence")
    print("component")
    print("exit")
    mode = input("Enter new mode:")


if __name__ == "__main__":
    process = None
    changeMode()
    while True:
        if(mode == "register"):
            try:
                process = register()
                process.registerTeams()
                process.registerStudents()
                process.registerProjects()
                process.updateDatabase()
            except KeyboardInterrupt:
                changeMode()
            except EOFError:
                print("Keyboard Interrupt!")
                print("Exitting ...")
                exit()
            except:
                print("Error ...")
                print("Exitting ...")
                exit()
        elif(mode == "attendence"):
            try:
               process = attendence()
               process.updateDatabase()
            except KeyboardInterrupt:
                changeMode()
            except:
                print("Error ...")
                print("Exitting ...")
                exit()
        elif(mode == "component"):
            try:
                process = component()
                process.showData()
                process.updateDatabase()
            except KeyboardInterrupt:
                changeMode()
            except BaseException as e:
                print("Error ...",str(e))
                print("Exitting ...")
                exit()
        elif(mode == "exit"):
            exit()
        else:
            changeMode()
else:
    print("Does not support being imported as a module")