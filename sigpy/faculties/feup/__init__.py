from sigpy.interface import interface
from sigpy.utils import get_school_year


class faculty(interface):
    def __init__(self, name, save_cache):
        super(faculty, self).__init__(name, save_cache)
