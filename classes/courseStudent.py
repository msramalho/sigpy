import sys
sys.path.append('../')
from classes.course import *

class courseStudent(course):
    def __init__(self, initials="", id="", cod="", name="", director="", directorAdj="", degree="", type="", start="", duration="", subjectsLink="", year="", state="", enrolled="", institution = ""):
        super(courseStudent, self).__init__(initials, id, cod, name, director, directorAdj, degree, type, start, duration, subjectsLink)
        self.year=year
        self.state=state
        self.enrolled=enrolled
        self.institution=institution
    
    def loadCourse(self, course):#copy the parameters from a course instance
        self.__dict__.update(course.__dict__)

    def __str__(self):
        return "Course %s: %s (%s)\nDirector:%s\nDirector Adj:%s\nDegree:%s\nType:%s\nStart:%s\nDuration:%s\n----\nEnrolled in %s year, status: %s, enrolled:%s, institution: %s" % (self.id, self.name, self.cod, self.director, self.directorAdj, self.degree, self.type, self.start, self.duration, self.year, self.state, self.enrolled, self.institution)