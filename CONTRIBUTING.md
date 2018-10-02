# Contributing
How you can help:
 1. Write examples using this tool for others to have a better work basis
 1. Improve the completeness of the tool (write or increment JSON classes, see how [below]())
 1. (Extend the tool to other faculties, mostly copy-paste and testing)
 1. Write tests for the existing code and also to your JSON contributions



## Project Organization
Before contributing, let's see how sigpy is organized.

Inside the sigpy folder you will find:
 * 📁 classes
    * [model.py](sigpy/classes/model.py) (wrapper class for parsed objects)
    * [picture.py](sigpy/classes/picture.py) (class for picture handling)
 * 📁 faculties (contains one folder per faculty)
    * 📁 feup (contains `.json` files specifying parsing rules)
        * [__init__.py](sigpy/faculties/feup/__init__.py) (simple subclass creation script, can be copy-pasted to other faculties)
        * course.json
        * room.json
        * student.json
        * ...
    * 📁 fcup ...
        * __init__.py
        * ...
    * ...

## How the Parsing Magic Works
Each faculty has its `.json` files that specify the "parseable" classes of that faculty. To add more fields or create new classes you just need to edit or create new `.json` files. The interface script takes care of finding them and creating the magical `get_CLASSNAME` from the `CLASSNAME.json` files!

Each of the `CLASSNAME.json` files has the following format:
```json
{
    "url": "the url for the page to parse, maybe with?get_parameters=1&...",
    "help": "This URL requires: (tuple of GET parameters needed)",
    "picture": "picture (this is optional and usually just for people)",
    "attributes": {
        "attr1": {"css": "some css selector"},
        "attr2": {"regex": "some regex expression"},
        "attr3": {"xpath": "some xpath selector"},
        "attr4": {"derivate": "string for format, eg: up%s@fe.up.pt for email", "from": ["attr1"]},
        "attr5": {"css|regex|xpath": "if we only care about if it was empty or not,
			regex must include a catch group", "boolean": "True"},
        "attr6": {
            "list": "True",
            "model": "a list of what?",
            "css": "to find the first element, ",
            "attributes: {
                ...
            }
        }
        ...
    }
}
```
Some notes:
 * The attributes can be extracted through css selectors, regex expressions and xpath selectors, which is enough for most tasks (so far nothing has been impossible to parse with them).
 * The attributes can be lists, for instance a student can have a list of courses it has enrolled in, etc...
 * notice that it is recursive and one attribute can be a model and have some other attribute that is also a model, _ad infinitum_.


Here is a complete example of a `faculties/feup/student.json` file with useful comments:
```python
{
"url": "https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=%s",
"help": "This URL requires: (student_id)",
# url for getting pictures
"picture": "https://sigarra.up.pt/feup/pt/fotografias_service.foto?pct_cod=%s",
"attributes": { # attributes a student can have
    # the name is filtered through a css selector
    "name": {"css": "div.estudante-info-nome"},

    # the same goes for id
    "id": {"css": "div.estudante-info-numero a"},

    # derivate means it will be formatted using another attribute after loading
    # using python formatting features like: student.email = "up%s@fe.up.pt" % student.id
    # this is a rare attribute type
    "email": {"derivate": "up%s@fe.up.pt", "from": ["id"]},

    "courses": { # if the attribute is a list instead of a value
        "model": "course",  # model works as class
        "list": "True",  # omission means single, so this is a list of "course"

        # how to find each element of the list to iterate
        "css": "div.estudante-lista-curso-activo",
        # this is just as the student model, its just inside another model, recursivity!!
        "attributes": {
            "name": {"css": "div.estudante-lista-curso-nome"},
            "institution": {"css": "div.estudante-lista-curso-instit"},

            # in this case REGEX is used to search the HTML for
            # the attribute id (must be in a REGEX capture group)
            "id": {"regex": ".*pv_curso_id=(\d+).*"},

            # if CSS and REGEX are not enough, you can get all the power of XPATH
            "enrolled": {"xpath": ".//td[text()='Ano da primeira inscrição:']/following::td[1]"},
            "year": {"xpath": ".//td[text()='Ano curricular atual:']/following::td[1]"},
            "state": {"xpath": ".//td[text()='Estado atual:']/following::td[1]"}
        }
    },
    "inactive_courses": { # Another attribute that is a list
        "model": "course",
        "list": "True",
        "css": "div.tabela-longa",
        "attributes": {
            "name": {"css": "td.t.k"},
            "id": {"regex": ".*pv_curso_id=(\d+).*"},
            "institution": {"xpath": ".//tr[@class='i']/td[2]/a/@title"},
            "old_id": {"css": "td.l"},
            "type": {"css": "td.t", "index": 2},
            "started": {"css": "td.l", "index": 1}
        }
    }
}
```
