import sys, requests, re
sys.path.append('../')
from utils import *
from bs4 import BeautifulSoup
#this class defines all the variables and methods that the faculty class should implement
notImplementedWarning = "\nMethod not implemented for %s module\n"
class interface:
    def __init__(self, name, defaultLoads = False):#defaultLoads is the value for the self.loadXXXX variables
        self.name = name
        self.session = requests
        self.orcid = "http://orcid.org/%s"
        self.base = self.index = self.pictures = self.courses = self.students = self.teachers= "not set for this faculty"
        self.loadCourses = self.loadTeachers = self.loadSubjects = defaultLoads

    def setLoad(self, name, value):
        self.__dict__[name] = value

    def startSession(self, username, password):#creates a requests session to access protecte pages
        print(notImplementedWarning % self.name)

    def __str__(self):
        return notImplementedWarning % self.name

    def getPicture(self, id=""):#reads the picture from the web and returns it, if it exists
        print(notImplementedWarning % self.name)

    def findStudent(self, id):#sends get request for the student id and parses his/her information
        print(notImplementedWarning % self.name)

    def findTeacher(self, id):#sends get request for the teacher id and parses his/her information
        print(notImplementedWarning % self.name)

    def findCourse(self, id):#creates a course instance from the course id
        print(notImplementedWarning % self.name)

    def findRoom(self, id):#creates a room instance from the room id
        print(notImplementedWarning % self.name)

    def findSubjects(self, id):#creates a subject instance from the subject id
        print(notImplementedWarning % self.name)

    def findSubject(self, id):#creates a subject instance from the subject id
        print(notImplementedWarning % self.name)

    def evalSession(self, functionName):#checks if a valid session exists and exits if not
        if self.session == requests:
            print("\nERROR - The % function requires a user session\n call startSession(username, password) for this purpose" % functionName)
    def checkSession(self):#checks if a valid session exists and exits if not
        if self.session == requests:
            return False
        return True