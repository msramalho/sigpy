import sys
sys.path.append('../')
from classes.person import *
from classes.courseStudent import *

class student(person):
    def __init__(self, dictionary):
        super(student, self).__init__(dictionary)
