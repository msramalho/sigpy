import sys
sys.path.append('../')
from classes.person import *
from classes.courseStudent import *

class student(person):
    def __init__(self, id="", name="unknown", emails = [], picture = None, courses = []):
        super(student, self).__init__(id,name,emails,picture)
        self.courses = courses

        
    def __str__(self):
        res = "UP%s - %s, emails:%s, picture=%s, courses (%d):\n" % (self.id, self.name, tuple(self.emails), self.picture, len(self.courses))
        i=0
        for c in self.courses:
            i+=1
            res += "\n\nCOURSE "+str(i)+"\n" + str(c)
        return res