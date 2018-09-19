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
from lxml.cssselect import CSSSelector as css
from lxml import etree
from bs4 import BeautifulSoup

from sigpy.classes.picture import picture
from sigpy.parser import parse_attributes, get_class_from_dict


# this class defines all the variables and methods that the faculty class should implement
class interface:
    configs = {
        "auth": "https://sigarra.up.pt/feup/pt/vld_validacao.validacao",
        "auth_failed": "O conjunto utilizador/senha não é válido."
    }

    classes = {}  # this is the property set from the JSON files

    def __init__(self):
        self.session = requests

    def get_class(self, class_name, route_tuple, original=None):
        config = interface.classes[class_name]
        try:
            url = config["url"] % route_tuple  # format the url with the given data
        except Exception as e:
            print("[-] Error: %s in formatting URL with your tuple %s: \n    %s" % (str(e), route_tuple, config["help"]))
        req = self.session.get(url)  # perform the request
        if req.status_code != 200:  # if request fails, display the error code (404, ...)
            print("[-] [%s] status code on:\n    %s" % (req.status_code, url))
        tree = fromstring(req.text)
        return get_class_from_dict(class_name, parse_attributes(tree, config["attributes"], original))

    # static method that receives an id and returns the numeric part
    def get_id(id):
        if isinstance(id, str) and "up" in id.lower():
            return id[2:]
        return id

    # reads a picture from the web and returns it, if it exists, m is a model instance
    def get_picture(self, m):
        if "picture" in interface.classes[m.class_name]:  # this instance has picture
            route = interface.classes[m.class_name]["picture"]
            pid = getattr(m, "picture_id", m.id)
            r = self.session.get(route % str(pid), stream=True)
            # path = "%s.jpg" % pid
            # print(path)
            if r.status_code == 200:
                return picture("%s.jpg" % pid, r.raw)
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
        def _get_method(id, original=None):
            thing = self.get_class(name, interface.get_id(id), original)
            thing.id = id if type(id) is not tuple else id[0]
            return thing
        return _get_method


# this function is used to dynamically select the appropriate faculty and load its values from the JSON mappings
def get_faculty(faculty="feup"):
    if not os.path.isfile("sigpy/faculties/%s/__init__.py" % faculty):  # faculty not implemented
        raise Exception("The faculty %s has not been implemented" % faculty)
    mod = importlib.import_module("sigpy.faculties.%s" % faculty)  # import the correct module
    fac = mod.faculty()  # create an instance of the correct faculty
    fac.name = faculty  # set its name, only for user advantage reasons

    # find all the JSON files inside the faculty folder
    file_list = glob.glob('sigpy/faculties/%s/*.json' % faculty)
    for filename in file_list:  # iterate over the files
        # for each, read contents, parse the JSON and load it into fac.classes for interface to use
        with open(filename, encoding="utf-8") as f:
            model = splitext(basename(filename))[0]  # get the model name from the filename
            json_data = json.load(f)
            fac.classes[model] = json_data
            setattr(fac, "get_%s" % model, fac.create_dynamic_method(model))
    return fac
