# Contributing

Essentially, there is a lot to do, most of it is _web scraping_ work:
 - Add more fields to current classes
 - Create new classes
 - Create new classes for other faculties (only feup supported at the moment)
If you have some of the following skills, you can help already:
 - Knowledge of HTML
 - Knowledge of CSS selectors
 - Knowledge of REGEX
 - Knowledge of XPATH
 - Knowledge of Python
 - Add more tests to our test suite

## Project Organization
Inside the sigpy folder you will find:
 * 📁 classes
    * [model.py](sigpy/classes/model.py) (wrapper class for parsed objects)
    * [picture.py](sigpy/classes/picture.py) (class for picture handling)
 * 📁 faculties (contains one folder per faculty)
    * 📁 feup (contains `.json` files specifying parsing rules)
        * [__init__.py](sigpy/faculties/feup/__init__.py) (file where the urls are defined as they can be dynamic)
        * course.json
        * room.json
        * student.json
        * ...
    * 📁 fcup ...
        * __init__.py
        * ...
    * ...

## How the Parsing Magic Works
Each of the `class.json` files has the following format:
```json
{
	"url": "____",
    "help": "This URL requires: (tuple of GET parameters needed)",
    "picture": "picture (this is optional and usually just for people)",
    "attributes": {
        "attr1": {"css": "some css selector"},
        "attr2": {"regex": "some regex expression"},
        "attr3": {"xpath": "some xpath selector"},
        "attr4": {"derivate": "string for format, eg: up%s@fe.up.pt for email", "from": ["attr1"]},
        "attr5": {"css|regex|xpath": "if we only care about if it was empty or not, regex must include a catch group", "boolean": "True"},
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

Notice that it is recursive and one attribute can be a model and have some other attribute that is also a model, _ad infinitum_.

```python
{
    "url": "student", # url name for loading this resource (it is not here because JSON is static)
    "picture": "picture",  # url name for getting pictures
    "attributes": { # attributes a student can have
        "name": {"css": "div.estudante-info-nome"},  # the name is filtered through a css selector
        "id": {"css": "div.estudante-info-numero a"}, # the same goes for id
        "email": {"derivate": "up%s@fe.up.pt", "from": ["id"]},  # derivate means it will be formatted using another attribute after loading, using python formatting features like: student.email = "up%s@fe.up.pt" % student.id
        # this is a rare attribute type
        "courses": { # if the attribute is a list instead of a value
            "model": "course",  # model works as class
            "list": "True",  # omission means single, so this is a list of "course"
            "css": "div.estudante-lista-curso-activo", # how to find each eleement of the list to iterate
            "attributes": { # this is just as the student model, its just inside another model, recursivity!!
                "name": {"css": "div.estudante-lista-curso-nome"},
                "institution": {"css": "div.estudante-lista-curso-instit"},
                "id": {"regex": ".*pv_curso_id=(\d+).*"},  # in this case REGEX is used to search the HTML for the attribute id (must be in a REGEX capture group)
                "enrolled": {"xpath": ".//td[text()='Ano da primeira inscrição:']/following::td[1]"}, # if CSS and REGEX are not enough, you can get all the power of XPATH
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
}
```