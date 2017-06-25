import sys, os
sys.path.append('../')
from utils import constructString
from PIL import Image
class picture:
    def __init__(self, path=""):
        self.path = path

    def exists(self):
        return os.path.isfile(self.path)

    def show(self):
        exists = self.exists()
        if exists:
            img = Image.open(self.path)
            img.show()
        else:
            print("Unable to show image (%s) - file deleted" % self.path)
        return exists

    def delete(self):
        os.unlink(self.path)
    def __str__(self):
        return constructString(self)
        