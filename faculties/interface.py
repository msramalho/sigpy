import sys
import requests
import re
import os
import shutil
from getpass import getpass
from lxml.html import fromstring, HtmlElement
from lxml.cssselect import CSSSelector as css
from lxml import etree
from bs4 import BeautifulSoup

sys.path.append('../')
from classes.model import model
from classes.picture import picture
from faculties.parser import parse_attributes, get_class_from_dict
# this class defines all the variables and methods that the faculty class should implement
notImplementedWarning = "\nMethod not implemented for %s module\n"


class interface:
    name = "interface"
    routes = {
        "orcid": "http://orcid.org/%s",
        "base": False,
        "index": False,
        "picture": False,
        "course": False,
        "student": False,
        "teacher": False,
        "base": False,
        "auth": "https://sigarra.up.pt/feup/pt/vld_validacao.validacao"
    }

    configs = {
        "pictures_folder": "./images/",
        "auth_failed": "O conjunto utilizador/senha não é válido."
    }

    classes = {
        "student": {
            "url": "student",
            "attributes": {
                "name": {"css": "div.estudante-info-nome"},  # if not class in attribute
                "courses": {
                    "class": "course",
                    "list": True,  # omission means single
                    "css": "div.estudante-lista-curso-activo",
                    "attributes": {
                        "name": {"css": "div.estudante-lista-curso-nome"},
                        "id": {"regex": ".*pv_curso_id=(\d+).*"},  # if there is an anchor
                        "enrolled": {"xpath": ".//td[text()='Ano da primeira inscrição:']/following::td[1]"},
                        "year": {"xpath": ".//td[text()='Ano curricular atual:']/following::td[1]"},
                        "state": {"xpath": ".//td[text()='Estado atual:']/following::td[1]"}
                    }
                },
                "inactive_courses": {
                    "class": "course",
                    "list": True,  # omission means single
                    "css": "div.tabela-longa",
                    "attributes": {
                        "name": {"css": "td.t.k"},
                        "id": {"regex": ".*pv_curso_id=(\d+).*"},  # if there is an anchor
                        "institution": {"xpath": ".//tr[@class='i']/td[2]/a/@title"}
                    }
                }
            }
        },
        "course": {
            "url": "course"
        }
    }

    def __init__(self):  # defaultLoads is the value for the self.loadXXXX variables
        self.session = requests

    def get_class(self, class_name, route_tuple):
        conf = interface.classes[class_name]
        req = self.session.get(interface.routes[conf["url"]] % route_tuple)
        tree = fromstring(req.text)
        return get_class_from_dict(class_name, parse_attributes(tree, conf["attributes"]))

    def get_student(self, id):
        student = self.get_class("student", (id))
        student.id = id
        return student

    # reads the picture from the web and returns it, if it exists
    def get_picture(self, id):
        r = self.session.get(interface.routes["picture"] % str(id), stream=True)
        path = "%s%s.jpg" % (interface.configs["pictures_folder"], id)
        if r.status_code == 200:
            return picture(os.path.abspath(path), r.raw)
        return False

    # log a user in, either receive or prompt for password, tests using configs["auth_failed"]
    def login(self, username, password=None):  # creates a requests session to access protected pages
        if password is None:
            password = getpass("Password for %s?\n" % username)
        self.session = requests.Session()
        payload = {'p_user': username, 'p_pass': password}
        r = self.session.post(interface.routes["auth"], params=payload)
        if re.search(interface.configs["auth_failed"], r.text):
            self.session = requests
            return False
        return True

    # checks if a valid session exists and exits if not
    def logged_in(self):
        return self.session != requests
