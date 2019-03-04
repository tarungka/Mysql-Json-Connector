#!/usr/bin/python3
import json
import os
message = """\t\t\tWELCOME TO RAIL REGISTRAION\nStuents can register as groups of 2 or 4."""
class cli:
    def __init__(self):
        print(message)
        print("\t\t\tTEAM REGISTRATION")
        self.numberOfStudents = int(input("Enter the number of students(either 2 or 4)  :"))
        self.teamName =                  input("Enter team name(given by sir/admin)          :")
        self.projectName =               input("Name of the project                          :")

    def generateRailId(self,usn):
        rail_id = 'R' + usn[-9:]
        return str(rail_id)

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
        header = '{"HEADER" : {"DATABASE" : "rail_db","TABLE_NAME" : "cur_studs","REQUEST_TYPE" : "insert"},'
        firstHalf = '"DATA":{"FIELDS":'
        secondHalf = json.dumps(inputDict)
        thirdHalf = ',"SET" : null,"WHERE" : null},'
        footer = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'
        return (header + firstHalf + secondHalf + thirdHalf + footer)

    def generateArgumentForTeam(self,inputDict):
        header = '{"HEADER" : {"DATABASE" : "rail_db","TABLE_NAME" : "cur_teams","REQUEST_TYPE" : "insert"},'
        firstHalf = '"DATA":{"FIELDS":'
        secondHalf = json.dumps(inputDict)
        thirdHalf = ',"SET" : null,"WHERE" : null},'
        footer = '"FOOTER" : {"DATA ABOUT THE REQUEST" : "just a test","COMMENT" : "THIS IS A TEST","DEP" : null,"UPDATE" : null}}'
        return (header + firstHalf + secondHalf + thirdHalf + footer)

    def generateArgumentForProject(self,inputDict):
        header = '{"HEADER" : {"DATABASE" : "rail_db","TABLE_NAME" : "cur_projs","REQUEST_TYPE" : "insert"},'
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
            os.system("./newdatabase.py '" + studentArgument + "'")
        teamArgument    = self.generateArgumentForTeam(self.team)
        projectArgument = self.generateArgumentForProject(self.project)
        os.system("./newdatabase.py '" + teamArgument + "'")
        os.system("./newdatabase.py '" + projectArgument + "'")

if __name__ == "__main__":
    process = cli()
    process.registerTeams()
    process.registerStudents()
    process.registerProjects()
    process.updateDatabase()
else:
    print("Does not support being imported as a module")