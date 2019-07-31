#!/usr/bin/python3
import json
import os
import datetime
import logging

"""
I NEED TO ADD VALIDATION HERE AS THE DATABASE.PY ONLY THE DATA INPUT
ASAP:ADD VALIDATION HERE!!!!
"""







logging.basicConfig(
        filename='railApplication.log',
        format='%(asctime)s.%(msecs)03d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

mode = "register"
message = """\t\t\tWELCOME TO RAIL REGISTRAION\nStuents can register as groups of 2 or 4."""

currentDatabase = list(json.load(open(".config/database.json"))["databases"].keys())[0]


class register:
    def __init__(self):
        global currentDatabase
        print(message)
        print("\t\t\tTEAM REGISTRATION")
        logging.info("Getting basic information")
        self.numberOfStudents = int(input("Enter the number of students(either 2 or 4)  :"))
        self.teamName =                  input("Enter team name(given by sir/admin)          :")
        self.projectName =               input("Name of the project                          :").upper()
        self.current_db = currentDatabase

    def validateUSN(self,usn):
        logging.info("Validating the usn")
        no    = usn[0]
        year  = usn[3:5]
        id    = usn[7:10]
        if(no.isdigit()):
            if(year.isdigit()):
                if(id.isdigit()):
                    logging.debug("Usn in valid")
                    return True
                else:
                    logging.debug("Usn in invalid")
                    return False
            else:
                logging.debug("Usn in invalid")
                return False
        else:
            logging.debug("Usn in invalid")
            return False
        

    def generateRailId(self,usn):
        logging.info("Generating rail id")
        try:
            assert (self.validateUSN(usn)),"INVALID USN!"
            rail_id = 'R' + usn[-9:]
            return str(rail_id)
        except AssertionError as e:
            print("Error:",str(e))
            logging.debug("Assertion Error raised when validating USN")
            changeMode()

    def getStudentInformation(self,currentUsn):
        print("Enter the details of",currentUsn)
        name        =   input("Enter the student name   :").upper()
        usn         =   currentUsn.upper()
        print("Usn                      :"+usn)
        print("Rail id                  :"+self.generateRailId(usn))
        gender      =   input("Enter your gender        :").upper()
        dob         =   input("Enter your date of birth :")
        phNumber    =   input("Enter your phone number  :")
        email       =   input("Enter your email         :").upper()
        team        =   self.team["team_name"]
        print("Team                     :"+team)
        branch      =   input("Enter your branch        :").upper()
        role        =   input("Enter your role          :").upper()
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
        logging.info("Registering student(s)")
        self.students = []
        for student in self.team["team_members"]:
            self.students.append(self.getStudentInformation(student))
            logging.debug("Done registering a student")
    
    def registerTeams(self):
        logging.info("Registering a team")
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
        logging.info("Registering projects")
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
        self.project.update({"date_start"           : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

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
        #for student in self.students:
        #    print(student)
        #print(self.team)
        #print(self.project)
        logging.info("Updating the database")
        try:
            #
            #Add a buffer to check if  all the data is valid - I dont know what I'm doing at the time of typing this
            #
            for student in self.students:
                studentArgument = self.generateArgumentForStudent(student)
                logging.debug("arguments to register a student:"+str(studentArgument))
                os.system("./database.py '" + studentArgument + "'")
            teamArgument    = self.generateArgumentForTeam(self.team)
            logging.debug("arguments to register a team:"+str(teamArgument))
            projectArgument = self.generateArgumentForProject(self.project)
            logging.debug("arguments to register a project:"+str(projectArgument))
            os.system("./database.py '" + teamArgument + "'")
            os.system("./database.py '" + projectArgument + "'")
        except:
            print("MAJOR ERROR, THE DATABASE HAS BEEN CORRUPTED")

class attendence:
    def __init__(self):
        global currentDatabase
        logging.info("Getting information from user")
        print("\t\t\tATTENDENCE")
        self.railId =               input("Enter RAIL ID                                :").upper()
        self.action =               input("Login or Logout?                             :").upper()
        if(self.action == 'login'.upper()):
            self.team =                 input("Enter team name(given by sir/admin)          :").upper()
            self.reason =               input("Reason for attending rail                    :").upper()
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
        if(self.action == ("login".upper())):
            header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "attendence","REQUEST_TYPE" : "insert"},'
            firstHalf = '"DATA":{"FIELDS":'
            secondHalf = json.dumps(inputDict)
            thirdHalf = ',"SET" : null,"WHERE" : null},'
            footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "login","COMMENT" : "THIS IS A TEST","DEP" :'
            dep = '[{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id"],"SET":null,"WHERE":{"rail_id" : "' + self.railId + '","login_status":"NO"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null} \
            		},{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["component_status"],"SET":null,"WHERE":{"rail_id" : "' + self.railId + '","component_status":"NO"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
            footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"login_status":"YES"},"WHERE":{"rail_id":"' + self.railId +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
            return (header + firstHalf + secondHalf + thirdHalf + footer_1 + dep + footer_3)
        elif(self.action == ("logout".upper())):
            header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "attendence","REQUEST_TYPE" : "update"},'
            firstHalf = '"DATA":{"FIELDS":null'
            thirdHalf = ',"SET" : {"time_out": "' + self.getCurrentTime() + '"},"WHERE" : {"rail_id" : "' + self.railId + '","time_out":"NULL"}},'
            footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "logout","COMMENT" : "THIS IS A TEST","DEP" :'
            dep = '[{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id","login_status"],"SET":null,"WHERE":{"rail_id" : "' + self.railId + '","login_status":"YES"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
            footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"login_status":"NO"},"WHERE":{"rail_id":"' + self.railId +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "Just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
            return (header + firstHalf + thirdHalf + footer_1 + dep + footer_3)
        else:
            print("Something went wrong")

    def updateDatabase(self):
        logging.info("Updating the database")
        attendenceArgument = self.generateArgumentForAttendence(self.data)
        logging.debug("arguments for attendence is:"+str(attendenceArgument))
        try:
            os.system("./database.py '" + attendenceArgument + "'")
        except:
            print("MAJOR ERROR, THE DATABASE HAS BEEN CORRUPTED")

class component:
    def __init__(self):
        global currentDatabase
        logging.info("Getting basic information for components")
        print("\t\t\tCOMPONENT")
        self.numberOfComponents = int(input("Number of components                        :"))
        self.requestType        =     input("Request/Return?                             :").upper()
        self.issuedTo           =    input("Enter your rail_id                          :").upper()
        self.componentId = []
        for index in range(self.numberOfComponents):
            self.componentId.append(input("Enter the component id of component number %d:" % (index+1)).upper())
        if(self.requestType == "REQUEST"):
            self.associatedTeam     =    input("Enter your associated team                  :").upper()
        self.checkCompId()
        self.convertToData()
        self.current_db = currentDatabase

    def checkCompId(self):
        logging.info("Validating component Id")
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
                localDict.update({"time_of_return": "null"})
                self.data.append(localDict)


    def generateArgumentForComponent(self,data):
        localList = []
        if(self.requestType == "REQUEST"):
            for aData in data:
                #print(aData)
                header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "iss_compnts","REQUEST_TYPE" : "insert"},'
                firstHalf = '"DATA":{"FIELDS":'
                secondHalf = json.dumps(aData)
                thirdHalf = ',"SET" : null,"WHERE" : null},'
                footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "req_comp","COMMENT" : "THIS IS A TEST","DEP" :'
                dep = '[{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id"],"SET":null,"WHERE":{"rail_id" : "' + self.issuedTo + '","login_status":"YES"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
                #print("bf2")
                dep_2 = '},{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"components","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["component_id"],"SET":null,"WHERE":{"component_id" : "' + aData["component_id"] + '","component_status":"NO"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
                #print("af2")
                footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"component_status":"YES"},"WHERE":{"rail_id":"' + self.issuedTo +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'
                footer_4 = ',{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"components","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"component_status":"YES"},"WHERE":{"component_id":"' + aData["component_id"] +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
                localList.append((header + firstHalf + secondHalf + thirdHalf + footer_1 + dep + dep_2 + footer_3 + footer_4))
        elif(self.requestType == "RETURN"):
            for aData in data:
                #print(aData)
                header = '{"HEADER" : {"DATABASE" : "' + self.current_db + '","TABLE_NAME" : "iss_compnts","REQUEST_TYPE" : "update"},'
                firstHalf = '"DATA":{"FIELDS": null'
                thirdHalf = ',"SET" : {"time_of_return" : "' + self.getCurrentTime() + '"},"WHERE" : ' + json.dumps(aData) + '},'
                footer_1 = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "ret_comp","COMMENT" : "THIS IS A TEST","DEP" :'
                dep = '[{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"cur_studs","REQUEST_TYPE":"select"},"DATA":{"FIELDS": ["rail_id"],"SET":null,"WHERE":{"rail_id" : "' + self.issuedTo + '","login_status":"YES"}},"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}'
                footer_3 = '}],"UPDATE" : [{"HEADER":{"DATABASE":"' + self.current_db + '","TABLE_NAME":"components","REQUEST_TYPE":"update"},"DATA":{"FIELDS": null,"SET":{"component_status":"NO"},"WHERE":{"component_id":"' + aData["component_id"] +'"}},"FOOTER":{"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}]}}'
                localList.append((header + firstHalf + thirdHalf + footer_1 + dep + footer_3))
        return localList

    def updateDatabase(self):
        logging.info("Inside updateDatabase")
        componentArguments = self.generateArgumentForComponent(self.data)
        print("Number of components is:",len(componentArguments))
        try:
            for aData in componentArguments:
                logging.debug("argument to issue component-"+str(aData))
                os.system("./database.py '" + aData + "'")
        except:
            print("MAJOR ERROR, THE DATABASE HAS BEEN CORRUPTED")
            

    #def showData(self):
    #    print("numberOfComponents   :",self.numberOfComponents)
    #    print("request/return       :",self.requestType)
    #    for index in range(self.numberOfComponents):
    #        print(("component no %d       :") % (index+1),self.componentId[index])
        #print("numberOfComponents:",self.numberOfComponents)
        #print("numberOfComponents:",self.numberOfComponents)



def changeMode():
    global mode
    logging.info("Change mode was called.")
    print("The availabe modes are:")
    print("1->register")
    print("2->attendence")
    print("3->component")
    print("4->exit")
    mode = input("Enter new mode:")
    logging.warning("Changing mode to:"+str(mode))

logging.info("Start of railCli.py")
if __name__ == "__main__":
    logging.info("Was not imported as a module")
    process = None
    changeMode()
    while True:
        if(mode == "register" or mode == "1"):
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
            except BaseException as e:
                logging.error(str(e))
                print("Exitting ...")
                exit()
        elif(mode == "attendence" or mode == "2"):
            try:
               process = attendence()
               process.updateDatabase()
            except KeyboardInterrupt:
                changeMode()
            except BaseException as e:
                logging.error(str(e))
                print("Exitting ...")
                exit()
        elif(mode == "component" or mode == "3"):
            try:
                process = component()
                process.showData()
                process.updateDatabase()
            except KeyboardInterrupt:
                changeMode()
            except BaseException as e:
                logging.error(str(e))
                print("Exitting ...")
                exit()
        elif(mode == "exit" or mode == "4"):
            logging.info("Exitting the application")
            exit()
        else:
            changeMode()
        logging.debug("Completed a request")
else:
    print("Does not support being imported as a module")