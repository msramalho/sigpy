
from sigpy.interface import interface


class faculty(interface):
    def __init__(self, name, save_cache):
        super(faculty, self).__init__(name, save_cache)
