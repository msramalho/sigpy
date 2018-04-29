import sys
from lxml.html import fromstring, HtmlElement
from lxml.cssselect import CSSSelector as css
from lxml import etree
import re

sys.path.append('../')
from classes.model import model
# ROUTE PARSING FUCTIONS


# given a class name and a dict of attribute->value, create a new class (child of model) all the possibilities must be imported (TODO: use __init__.py)
def get_class_from_dict(class_name, dictionary):
    # klass = globals()[class_name]
    # return klass(dictionary)
    return model(class_name, dictionary)


# given an lxml tree and a config dict with a "regex" key, get its value
def parse_regex(tree, config):
    index = config["index"] if "index" in config else 1
    res = re.search(config["regex"], etree.tostring(tree,encoding='utf-8').decode("utf-8"))
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
    return get_class_from_dict(config["model"], d)


# primary function that receives a tree and recursively finds its values, returning accordingly
def parse_attributes(tree, attributes):
    res = {}
    for attr, config in attributes.items():
        if "model" not in config:  # this is a simple attr with direct css
            res[attr] = parse_attribute(tree, config)
        elif "model" in config:  # handle classes
            element = parse_element(tree, config)
            if "list" in config:  # handle list of said class
                res[attr] = [parse_class(e, config) for e in element]
            else:  # handle single element of that class
                res[attr] = parse_class(element, config)
    return res
