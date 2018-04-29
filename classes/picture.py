import sys
import os
from PIL import Image


class picture:
    def __init__(self, path, raw):
        self.img = Image.open(raw)
        self.path = path

    def show(self):
        self.img.show()
        return self

    def save(self):
        self.img.save(self.path)
        return self

    def delete(self):
        os.unlink(self.path)
        return self
