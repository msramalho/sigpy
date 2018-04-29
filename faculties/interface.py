import sys
import requests
import re
import os
import shutil
from getpass import getpass
from lxml.html import fromstring, HtmlElement
from lxml.cssselect import CSSSelector as css
from lxml import etree

sys.path.append('../')
from utils import *
from bs4 import BeautifulSoup
from classes.model import model
from classes.picture import picture
# this class defines all the variables and methods that the faculty class should implement
notImplementedWarning = "\nMethod not implemented for %s module\n"


# ROUTE PARSING FUCTIONS


# given a class name and a dict of attribute->value, create a new class (child of model) all the possibilities must be imported (TODO: use __init__.py)
def get_class_from_dict(class_name, dictionary):
    # klass = globals()[class_name]
    # return klass(dictionary)
    return model(class_name, dictionary)


# given an lxml tree and a config dict with a "regex" key, get its value
def parse_regex(tree, config):
    index = config["index"] if "index" in config else 1
    res = re.search(config["regex"], etree.tostring(tree).decode("utf-8"))
    if res:
        return res.group(index)
    return None


# given an lxml tree and a config dict with a "css" key, get its value
def parse_css(tree, config):
    index = config["index"] if "index" in config else 0
    return tree.cssselect(config["css"])[index].text_content().strip()


# given an lxml tree and a config dict with a "xpath" key, get its value
def parse_xpath(tree, config):
    index = config["index"] if "index" in config else 0
    el = tree.xpath(config["xpath"])[index]
    if isinstance(el, HtmlElement):
        el = el.text_content()
    return el.strip()


# given an lxml tree and a config dict with one of [css, regex, xpath] key, get its value
def parse_attribute(tree, config):
    if "css" in config:  # this is an attribute from css
        return parse_css(tree, config)
    elif "regex" in config:  # this is an attribute from regex
        return parse_regex(tree, config)
    elif "xpath" in config:
        return parse_xpath(tree, config)


# given an lxml tree and a config dict with one of [css, xpath] key, get its lxml element
def parse_element(tree, config):
    if "css" in config:  # this is an attribute from css
        return tree.cssselect(config["css"])
    elif "xpath" in config:
        return tree.xpath(config)


# given an lxml element and a config, parse a class's attributes and create a new class from them
def parse_class(element, config):
    d = parse_attributes(element, config["attributes"])
    return get_class_from_dict(config["class"], d)


# primary function that receives a tree and recursively finds its values, returning accordingly
def parse_attributes(tree, attributes):
    res = {}
    for attr, config in attributes.items():
        if "class" not in config:  # this is a simple attr with direct css
            res[attr] = parse_attribute(tree, config)
        elif "class" in config:  # handle classes
            element = parse_element(tree, config)
            if "list" in config:  # handle list of said class
                res[attr] = [parse_class(e, config) for e in element]
            else:  # handle single element of that class
                res[attr] = parse_class(element, config)
    return res


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

    def setLoad(self, name, value):
        self.__dict__[name] = value

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

    def __str__(self):
        return notImplementedWarning % self.name

    def checkSession(self):  # checks if a valid session exists and exits if not
        if self.session == requests:
            return False
        return True

    # reads the picture from the web and returns it, if it exists
    def get_picture(self, id):
        r = self.session.get(interface.routes["picture"] % str(id), stream=True)
        path = "%s%s.jpg" % (interface.configs["pictures_folder"], id)
        if r.status_code == 200:
            return picture(os.path.abspath(path), r.raw)
        return False
