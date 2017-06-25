import sys
sys.path.append('../')
from classes.course import *
class courseStudent(course):
    def __init__(self, initials="", id="", cod="", name="", degree="", type="", start="", duration="", subjectsLink="", year="", state="", enrolled="", institution = "", director="", directorAdj="", subjects = []):
        super(courseStudent, self).__init__(initials, id, cod, name, degree, type, start, duration, subjectsLink, director, directorAdj, subjects)
        self.institution=institution
        self.year=year
        self.enrolled=enrolled
        self.state=state
    
    def loadCourse(self, course):#copy the parameters from a course instance
        self.__dict__.update(course.__dict__)

    def __str__(self):
        return constructString(self)