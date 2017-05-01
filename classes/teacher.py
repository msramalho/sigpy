import sys
sys.path.append('../')
from classes.person import *

class teacher(person):
    def __init__(self, id="", name="unknown", emails = [], picture = None, initials = "", status="", phone="", voip="", rooms=[], category="", department = "", positions=[], description=""):
        teacher(student, self).__init__(id,name,emails,picture)
        self.initials = initials
        self.status = status
        self.phone = phone
        self.voip = voip
        self.rooms = rooms
        self.category = category
        self.department = department
        self.positions = positions
        self.description = description
        