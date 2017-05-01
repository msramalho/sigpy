import sys
sys.path.append('../')
from classes.person import *

class teacher(person):
    def __init__(self, id="", name="unknown", emails = [], picture = None, initials = "", status="", orcid="", phone="", voip="", rooms=[], category="", career="", department = "", section = "", positions=[], description="", schedule = ""):
        super(teacher, self).__init__(id,name,emails,picture)
        self.initials = initials
        self.status = status
        self.orcid = orcid
        self.phone = phone
        self.voip = voip
        self.rooms = rooms
        self.category = category
        self.career = career
        self.department = department
        self.section = section
        self.positions = positions
        self.description = description
        self.schedule = schedule
        