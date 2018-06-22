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
        "room": False,
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
                "id": {"css": "div.estudante-info-numero a"},
                "email": {"derivate": "up%s@fe.up.pt", "from": ["id"]},  # derivate from tuple #TODO: some students hay have different emails
                "courses": {
                    "model": "course",  # model works as class
                    "list": True,  # omission means single
                    "css": "div.estudante-lista-curso-activo",
                    "attributes": {
                        "name": {"css": "div.estudante-lista-curso-nome"},
                        "institution": {"css": "div.estudante-lista-curso-instit"},
                        "id": {"regex": ".*pv_curso_id=(\d+).*"},  # if there is an anchor
                        "enrolled": {"xpath": ".//td[text()='Ano da primeira inscrição:']/following::td[1]"},
                        "year": {"xpath": ".//td[text()='Ano curricular atual:']/following::td[1]"},
                        "state": {"xpath": ".//td[text()='Estado atual:']/following::td[1]"}
                    }
                },
                "inactive_courses": {
                    "model": "course",
                    "list": True,  # omission means single
                    "css": "div.tabela-longa",
                    "attributes": {
                        "name": {"css": "td.t.k"},
                        "id": {"regex": ".*pv_curso_id=(\d+).*"},  # if there is an anchor
                        "institution": {"xpath": ".//tr[@class='i']/td[2]/a/@title"},
                        "old_id": {"css": "td.l"},
                        "type": {"css": "td.t", "index": 2},
                        "started": {"css": "td.l", "index": 1}
                    }
                }
            }
        },
        "course": {
            "url": "course",
            "attributes": {
                "name": {"regex": "<title>FEUP - (.+)<\/title>"},
                "cod": {"xpath": ".//table[@class='formulario']/tr/td//text()[contains(., 'Código Oficial')]/following::td[1]"},
                "director": {
                    "model": "teacher",
                    "xpath": ".//table[@class='formulario']/tr[td[text()[contains(., 'Diretor:')]]]",
                    "attributes": {
                        "name": {"xpath": ".//td[2]"},
                        "id": {"regex": "pct_codigo=(.+?)\""}
                    }
                },
                "assistant_director": {
                    "model": "teacher",
                    "xpath": ".//table[@class='formulario']/tr[td[text()[contains(., 'Diretor Adjunto:')]]]",
                    "attributes": {
                        "name": {"xpath": ".//td[2]"},
                        "id": {"regex": "pct_codigo=(.+?)\""}
                    }
                }
            }
        },
        "teacher": {
            "url": "teacher",
            "attributes": {
                "name": {"regex": "<title>FEUP - (.*?)</title>"},
                "initials": {"xpath": ".//td[text()='Sigla:']/following::td[1]"},
                "state": {"xpath": ".//td[text()='Estado:']/following::td[1]"},
                "orcid": {"regex": "href=\"http://orcid.org/(.*?)\""},
                "alias": {"regex": ":(.*)'\+secure\+'fe\.up\.pt'"},
                "email": {"derivate": "%s@fe.up.pt", "from": ["alias"]},
                "phone": {"xpath": "(.//td[text()='Telefone:'])[2]/following::td[1]"},
                "voip": {"xpath": ".//td[text()='Voip:']/following::td[1]"},
                "category": {"xpath": ".//div[contains(@class, 'informacao-pessoal-funcoes')]//td[text()='Categoria:']/following::td[1]"},
                "presentation": {"css": "div.informacao-pessoal-apresentacao span"},
                "rooms": {
                    "model": "room",
                    "list": True,
                    "xpath": ".//td[text()='Salas: ']/following::td[1]",
                    "attributes": {
                        "name": {"css": "a.normal"},
                        "id": {"regex": "pv_id=(.*?)\""}
                    }
                },
                "positions": {
                    "model": "position",  # TODO: remove and make work
                    "list": True,
                    "css": "tr.k.d",
                    "attributes": {
                        "name": {"css": "td.k"},
                        "date": {"css": "td.l"},
                        "id": {"regex": "href=\".*=(.*?)\""}
                    }
                }
            }
        },
        "room": {
            "url": "room",
            "attributes": {
                "building": {"xpath": ".//div[text()='Edifício:']/following::div[contains(@class, 'form-campo')]"},
                "purpose": {"xpath": ".//div[text()='Utilização:']/following::div[contains(@class, 'form-campo')]"},
                "area": {"xpath": ".//div[contains(text(), 'Área')]/following::div[contains(@class, 'form-campo')]"},
                "phone": {"xpath": ".//div[text()='Telefone:']/following::div[contains(@class, 'form-campo')]"},
                "managers": {
                    "model": "teacher",  # may not be teacher, but rather superclass employee
                    "list": True,
                    "xpath": ".//div[text()='Responsáveis:']/following::div[contains(@class, 'form-campo')]/ul",
                    "attributes": {
                        "name": {"css": "li a"},
                        "id": {"regex": "href=\".*p_codigo=(.*?)\""}
                    }
                },
                "occupants": {
                    "model": "teacher",  # may not be teacher, but rather superclass employee
                    "list": True,
                    "xpath": ".//div[text()='Ocupante:']/following::div[contains(@class, 'form-campo')]/ul",
                    "attributes": {
                        "name": {"css": "li a"},
                        "id": {"regex": "href=\".*p_codigo=(.*?)\""}
                    }
                }
            }
        }
    }

    def __init__(self):  # defaultLoads is the value for the self.loadXXXX variables
        self.session = requests

    def get_class(self, class_name, route_tuple, original=None):
        conf = interface.classes[class_name]
        req = self.session.get(interface.routes[conf["url"]] % route_tuple)
        tree = fromstring(req.text)
        return get_class_from_dict(class_name, parse_attributes(tree, conf["attributes"], original))

    def get_student(self, id, original=None):
        student = self.get_class("student", (interface.get_id(id)), original)
        student.id = id
        return student

    def get_course(self, id, original=None):
        course = self.get_class("course", (interface.get_id(id)), original)
        course.id = id
        return course

    def get_teacher(self, id, original=None):
        teacher = self.get_class("teacher", (interface.get_id(id)), original)
        teacher.id = id
        return teacher

    def get_room(self, id, original=None):
        room = self.get_class("room", interface.get_id(id), original)
        room.id = id
        return room

    # static method that receives an id and returns the numeric part
    def get_id(id):
        if isinstance(id, str) and "up" in id:
            return id[2:]
        return id

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
