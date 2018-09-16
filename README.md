# Sigpy
This is a Sigarra Python API based on Recursive Web Scraping Parser (wtf). Essentially it performs requests as needed and parses the html information into objects you can use.

All of the main code is written and, other than bug fixing and enhancements, you will only need to edit `.json` files!


In the end, this is yet another Sigarra-based project that I wished existed before I needed something like it.

## Examples
Each example will hide all the code in the previous examples, the full script can be found [here]().

For all the examples below, you need to start by importing sigpy:

```python
from sigpy import get_faculty
```

### Login to your account
Give your id (with or without `up`) and either hardcode your password or wait for prompt:

```python
...
# get faculty object and login
fac = get_faculty("feup")

# login is optional but gives access to more information
fac.login("201403027", "youWish")

# if no password is given, secret prompt will appear
fac.login("up201403027")
```

### Extract Student Information

```python
...
# access student data from their id
# "up" is case insensitive and also optional
msramalho = fac.get_student("UP201403027")

# print a complete JSON view of student information
print(msramalho)

# or simply use the attribute you need
# a complete list is available in the JSON view
message = "Nice to meet you, %s" % msramalho.name
```

### Access Course Data

```python

# load mieic from the student (we know it is at index 1)
mieic = fac.get_course(msramalho.courses[1].id)

# print a complete JSON view of course information
print(mieic)
```

### Access Teacher Data

```python
# use the id of the course director to access teacher data!
# (the name of the variable may lose meaning in the future)
pascoal = fac.get_teacher(mieic.director.id)

# print a complete JSON view of teacher information
print(pascoal)
```

### Get Student, Teacher and Room Pictures
```python
# use the get_picture method with the object
# (temporarily download picture into a variable)
photo1 = fac.get_picture(msramalho)

# save the image locally on "./images/ID.jpg"
photo1.save()
# save the image locally on custom dir, absolute or relative
photo1.save("another/dir")

# you can do the same for teachers (and use chaining)
vidal = fac.get_teacher("206415")
fac.get_picture(vidal).show()
```
<p align="center"><img src="https://sigarra.up.pt/feup/en/FOTOGRAFIAS_SERVICE.foto?pct_cod=206415" height="200px"></p>

```python
# and even for room layout pictures
room = fac.get_room(vidal.rooms[0].id)
fac.get_picture(room).show()
```
<p align="center"><img src="https://sigarra.up.pt/feup/pt/instal_geral2.get_mapa?pv_id=77467" height="200px"></p>

## Contributing
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

#### Project Organization
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

each of the `class.json` files has the following format:
```json
{
    "url": "____",
    "picture": "picture (this is optional and usually just for people)",
    "attributes": {
        "attr1": {"css": "some css selector"},
        "attr2": {"regex": "some css selector"},
        "attr3": {"xpath": "some css selector"},
        "attr4": {"derivate": "some css selector", "from": ["attr1"]},
        "attr5": {
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
Notice that it is recursive and one attribute can be a model and have some other attribute that is also a model, _ad infinitum_
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