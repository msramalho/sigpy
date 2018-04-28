import sys
sys.path.append('../')
from classes.model import model
from utils import constructString


class person(model):
    def __init__(self, dictionary):
        super(person, self).__init__(dictionary)
        # self.id = id
        # self.name = name
        # self.emails = emails
        # self.picture = picture
