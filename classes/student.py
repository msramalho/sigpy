import sys
sys.path.append('../')
from classes.person import *
from classes.courseStudent import *

class student(person):
    def __init__(self, id="", name="unknown", emails = [], picture = None, courses = []):
        super(student, self).__init__(id,name,emails,picture)
        self.courses = courses

    def parse(self, html):
        print("PARSE Student")
        pass
        
        
    def __str__(self):
        return "UP%s - %s, emails:%s, picture=%s" % (self.id, self.name, tuple(self.emails), self.picture)