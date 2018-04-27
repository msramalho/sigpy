import sys
import requests
import re
import os
from getpass import getpass
sys.path.append('../')
from utils import *
from bs4 import BeautifulSoup
# this class defines all the variables and methods that the faculty class should implement
notImplementedWarning = "\nMethod not implemented for %s module\n"


class interface:
    routes = {
        "orcid": "http://orcid.org/%s",
        "base": False,
        "index": False,
        "pictures": False,
        "courses": False,
        "students": False,
        "teachers": False,
        "base": False,
        "auth": "https://sigarra.up.pt/feup/pt/vld_validacao.validacao"
    }

    configs = {
        "pictures_folder": "./images/",
        "auth_failed": "O conjunto utilizador/senha não é válido."
    }

    def __init__(self, name, defaultLoads=False):  # defaultLoads is the value for the self.loadXXXX variables
        self.name = name
        self.session = requests
        self.loadCourses = self.loadTeachers = self.loadSubjects = self.loadPictures = defaultLoads
        self.picturesFolder = "./images/"

    def setLoad(self, name, value):
        self.__dict__[name] = value

    def startSession(self, username, password=None):  # creates a requests session to access protected pages
        print(interface.routes)
        if password is None:
            password = getpass("Password for %s?\n" % username)
        self.session = requests.Session()
        payload = {'p_user': username, 'p_pass': password}
        r = self.session.post(interface.routes["auth"], params=payload)
        if re.search(interface.configs["auth_failed"], r.text):
            self.session = requests
            return False
        return True

    def findStudent(self, id):  # sends get request for the student id and parses his/her information
        print(self)

    def findTeacher(self, id):  # sends get request for the teacher id and parses his/her information
        print(self)

    def findCourse(self, id):  # creates a course instance from the course id
        print(self)

    def findRoom(self, id):  # creates a room instance from the room id
        print(self)

    def findSubjects(self, id):  # creates a subject instance from the subject id
        print(self)

    def findSubject(self, id):  # creates a subject instance from the subject id
        print(self)

    def getPicture(self, id="", path="", display=False, save=True):  # reads the picture from the web and returns it, if it exists
        print(self)

    """def evalSession(self, functionName):#checks if a valid session exists
        if self.session == requests:
            print("\nERROR - The % function requires a user session\n call startSession(username, password) for this purpose" % functionName)"""

    def __str__(self):
        return notImplementedWarning % self.name

    def checkSession(self):  # checks if a valid session exists and exits if not
        if self.session == requests:
            return False
        return True
