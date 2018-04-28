import sys
sys.path.append('../')
from classes.model import model
from utils import constructString

class course(model):
    def __init__(self, dictionary):
        super(course, self).__init__(dictionary)
        # self.name = name
        # self.initials = initials
        # self.id = id
        # self.cod = cod
        # self.director = director
        # self.directorAdj = directorAdj
        # self.degree = degree
        # self.type = type
        # self.start = start
        # self.duration = duration
        # self.subjectsLink = subjectsLink
        # self.subjects = subjects

    def findSubjects(self, fac):
        fac.findSubjects(self.subjectsLink)
