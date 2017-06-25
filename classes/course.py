import sys
sys.path.append('../')
from utils import constructString

class course:
    def __init__(self, initials="", id="", cod="", name="", degree="", type="", start="", duration="", subjectsLink=[""], director="", directorAdj="", subjects = []):
        self.name = name
        self.initials = initials
        self.id = id
        self.cod = cod
        self.director = director
        self.directorAdj = directorAdj
        self.degree = degree
        self.type = type
        self.start = start
        self.duration = duration
        self.subjectsLink = subjectsLink
        self.subjects = subjects
    
    def findSubjects(self, fac):
        fac.findSubjects(self.subjectsLink)

    def __str__(self):
        return constructString(self)