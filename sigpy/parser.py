import sys
import re
from lxml.html import fromstring, HtmlElement
from lxml.cssselect import CSSSelector as css
from lxml import etree

from sigpy.classes.model import model


# ROUTE PARSING FUNCTIONS
# given a class name and a dict of attribute->value, create a new class (child of model) all the possibilities must be imported (TODO: use __init__.py)
def get_class_from_dict(class_name, dictionary):
    return model(class_name, dictionary)


# given a config and a default value for index, either return the one in config or the default
def get_index(config, default=0):
    return config["index"] if "index" in config else default


# given an lxml tree and a config dict with a "regex" key, get its VALUE
def parse_regex(tree, config):
    res = re.search(config["regex"], etree.tostring(tree, encoding='utf-8').decode("utf-8"))
    if res:
        return res.group(get_index(config, 1))
    return None


# given an lxml tree and a config dict with a "css" key, get its VALUE
def parse_css(tree, config):
    return tree.cssselect(config["css"])[get_index(config)].text_content().strip()


# given an lxml tree and a config dict with a "xpath" key, get its VALUE
def parse_xpath(tree, config):
    el = tree.xpath(config["xpath"])[get_index(config)]
    if isinstance(el, HtmlElement):
        el = el.text_content()
    return el.strip()


# given a config dict with string "derivate" and tuple "from", match both and return
def parse_derivate(config, res):
    return config["derivate"] % tuple(res[t_el] for t_el in config["from"])


# given an lxml tree and a config dict with one of [css, regex, xpath] key, get its VALUE
def parse_attribute(tree, config, res):
    try:
        if "css" in config:  # this is an attribute from css
            return parse_css(tree, config)
        elif "regex" in config:  # this is an attribute from regex
            return parse_regex(tree, config)
        elif "xpath" in config:  # this is an attirbute from xpath
            return parse_xpath(tree, config)
        elif "derivate" in config:  # this is an attribute derivated from another
            return parse_derivate(config, res)
    except Exception as e:  # some attributes do not exist if not logged in
        print("[-] Error: %s when parsing %s... \n    Ignoring attribute - may be due to lack of login" % (str(e), config))
        return None


# given an lxml tree and a config dict with one of [css, xpath] key, get its lxml ELEMENT
def parse_element(tree, config):
    try:
        if "css" in config:  # this is an attribute from css
            return tree.cssselect(config["css"])
        elif "xpath" in config: # xpath always returns a list, so an extra step is needed
            res = tree.xpath(config["xpath"])
            return res[get_index(config)] if "list" not in config else res
    except Exception as e:  # some attributes do not exist if not logged in
        print("[-] Error: %s when parsing %s... Ignoring element" % (str(e), config))
        return []


# given an lxml element and a config, parse a class's attributes and create a new class from them
def parse_class(element, config):
    d = parse_attributes(element, config["attributes"])
    return get_class_from_dict(config["model"], d)


# primary function that receives a tree and recursively finds its values, returning accordingly
def parse_attributes(tree, attributes, original=None):
    res = {}
    for attr, config in attributes.items():
         # if the original already has the attribute defined then simple load it
        if original and attr in original.__dict__:
            res[attr] = original.__dict__[attr]
            continue
        # else load from the configurations
        if "model" not in config:  # this is a simple attr with direct css
            res[attr] = parse_attribute(tree, config, res)
            if "boolean" in config:  # we only want a yes or no value
                res[attr] = res[attr] is not None
        elif "model" in config:  # handle classes
            element = parse_element(tree, config)
            if "list" in config:  # handle list of said class
                res[attr] = [parse_class(e, config) for e in element]
            else:  # handle single element of that class
                res[attr] = parse_class(element, config)
    return res
