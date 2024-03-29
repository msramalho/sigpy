import sys
import os
from os.path import basename, splitext
import re
import requests
import importlib
import json
import glob

from getpass import getpass
from lxml.html import fromstring, HtmlElement

from . classes import picture, timetable
from . parser import parse_attributes, get_class_from_dict
from . utils import get_school_year, vprint, set_verbose
from . cache import cache


# this class defines all the variables and methods that the faculty class should implement
class interface:
    configs = {
        "auth": "https://sigarra.up.pt/feup/pt/vld_validacao.validacao",
        "auth_failed": "O conjunto utilizador/senha não é válido."
    }

    classes = {}  # this is the property set from the JSON files

    def __init__(self, faculty, save_cache):
        self.session = requests
        self.name = faculty
        self.cache = cache(self.name, save_cache)

    def set_verbose(self, verbose):
        set_verbose(verbose)

    def get_class(self, class_name, route_tuple, original=None, use_cache=True):
        config = interface.classes[class_name]
        try:
            url = config["url"] % route_tuple  # format the url with the given data
        except Exception as e:
            raise Exception("[-] Error: %s in formatting URL with your tuple %s: \n    %s" % (str(e), route_tuple, config["help"]))
        tree = fromstring(self.GET(url, use_cache))
        return get_class_from_dict(class_name, parse_attributes(tree, config["attributes"], original))

    # helper method to perform and debug requests on failure
    def GET(self, url, use_cache):
        return self.cache.get(self.session, url, use_cache)

    # static method that receives an id and returns the numeric part
    def get_id(id):
        if isinstance(id, str) and "up" in id.lower():
            return id[2:]
        return id

    # reads a picture from the web and returns it, if it exists, m is a model instance
    def get_picture(self, m):
        if "picture" in interface.classes[m.class_name]:  # this instance has picture
            route = interface.classes[m.class_name]["picture"]
            pid = getattr(m, "picture_id", interface.get_id(m.id))
            r = self.session.get(route % str(pid), stream=True)
            if r.status_code == 200:
                return picture("%s.jpg" % pid, r.raw)
        return False

    # parses a timetable from the web and returns it, if it exists, m is a model instance
    def get_timetable(self, m, school_year=get_school_year(), use_cache=True):
        if "timetable" in interface.classes[m.class_name]:  # this instance has a timetable
            route = interface.classes[m.class_name]["timetable"] % (m.id, school_year)
            return timetable(self.GET(route, use_cache))
        return False

    # log a user in, either receive or prompt for password, tests using configs["auth_failed"]
    def login(self, username, password=None):  # creates a requests session to access protected pages
        if password is None:
            password = getpass("Password for %s?\n" % username)
        self.session = requests.Session()
        payload = {'p_user': username, 'p_pass': password}
        r = self.session.post(interface.configs["auth"], params=payload)
        if re.search(interface.configs["auth_failed"], r.text):
            self.session = requests
            return False
        return True

    # checks if a valid session exists and exits if not
    def logged_in(self):
        return self.session != requests

    # add a method get_something(id, original=True) to itself where "something" is a string
    def create_dynamic_method(self, name):
        def _get_method(id, original=None, use_cache=True):
            thing = self.get_class(name, interface.get_id(id), original, use_cache)
            thing.id = id if type(id) is not tuple else id[0]
            return thing
        return _get_method


# this function is used to dynamically select the appropriate faculty and load its values from the JSON mappings
def get_faculty(faculty="feup", save_cache=True):
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), "faculties/%s/__init__.py" % faculty)):  # faculty not implemented
        raise Exception("The faculty %s has not been implemented" % faculty)
    mod = importlib.import_module("sigpy.faculties.%s" % faculty)  # import the correct module
    fac = mod.faculty(faculty, save_cache)  # create an instance of the correct faculty

    # find all the JSON files inside the faculty folder
    file_list = glob.glob(os.path.join(os.path.dirname(__file__), 'faculties/%s/*.json' % faculty))
    for filename in file_list:  # iterate over the files
        # for each, read contents, parse the JSON and load it into fac.classes for interface to use
        with open(filename, encoding="utf-8") as f:
            model = splitext(basename(filename))[0]  # get the model name from the filename
            json_data = json.load(f)
            fac.classes[model] = json_data
            setattr(fac, "get_%s" % model, fac.create_dynamic_method(model))
    return fac
