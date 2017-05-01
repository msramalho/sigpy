import sys
sys.path.append('../')
from classes.course import *

class courseStudent(course):
    def __init__(self, id="", name="", year="", state="", enrolled="", institution = ""):
        super(courseStudent, self).__init__(id=id, name=name)
        self.year=year
        self.state=state
        self.enrolled=enrolled
        self.institution=institution
