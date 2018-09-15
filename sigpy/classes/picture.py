import sys
import os
from PIL import Image

SAVE_TO = "images/"


class picture:

    def __init__(self, path, raw):
        self.img = Image.open(raw)
        self.path = path

    def show(self):
        self.img.show()
        return self

    def save(self, save_to=SAVE_TO):
        if not os.path.exists(save_to):
            os.makedirs(save_to)
        self.img.save(os.path.abspath(save_to + "/" + self.path))
        return self

    def delete(self):
        os.unlink(self.path)
        return self
