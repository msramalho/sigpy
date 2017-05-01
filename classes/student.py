import sys
sys.path.append('../')
from classes.person import *
from classes.courseStudent import *

class student(person):
    def __init__(self, id="", name="unknown", emails = [], picture = None, courses = []):
        super(student, self).__init__(id,name,emails,picture)
        self.courses = courses
