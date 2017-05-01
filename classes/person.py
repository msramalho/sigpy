import sys
sys.path.append('../')
from utils import constructString
class person:
    def __init__(self, id="", name="unknown", emails = [], picture = None):
        self.id = id
        self.name = name
        self.emails = emails
        self.picture = picture

    def __str__(self):
        return constructString(self)
        