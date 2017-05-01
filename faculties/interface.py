import requests, re
from bs4 import BeautifulSoup
#this class defines all the variables and methods that the faculty class should implement
notImplementedWarning = "\nMethod not implemented for %s module\n"
class interface:
    def __init__(self, name):
        self.name = name
        self.session = None
        self.index = self.pictures = self.courses = self.students = self.teachers= "not set for this faculty"

    def startSession(self, username, password):#creates a requests session to access protecte pages
        print(notImplementedWarning % self.name)

    def __str__(self):
        return notImplementedWarning % self.name

    def getPicture(self, id=""):#reads the picture from the web and returns it, if it exists
        print(notImplementedWarning % self.name)

    def findStudent(self, id):#sends get request for the student id and parses his/her information
        print(notImplementedWarning % self.name)
        
    def findCourse(self, id):#creates a course instance from the course id
        print(notImplementedWarning % self.name)

    def checkSession(self, functionName):#checks if a valid session exists and exits if not
        if self.session is None:
            print("\nERROR - The % function requires a user session\n call startSession(username, password) for this purpose" % functionName)