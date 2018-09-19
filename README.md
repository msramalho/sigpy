# Sigpy
This is a Sigarra Python API based on Recursive Web Scraping Parser (wtf). Essentially, it performs requests as needed and parses the html information into objects you can use.

All of the main code is written and, other than bug fixing and enhancements, you will only need to edit `.json` files!


In the end, this is yet another Sigarra-based project that I wished existed before I needed something like it.

# Examples
Each example will hide all the code of the previous examples.

For all the examples below, you need to start by importing sigpy:

```python
from sigpy import get_faculty
```

### Login to your account
Give your id (with or without `up`) and either hardcode your password or wait for prompt:

```python
# get faculty object and login
fac = get_faculty("feup")

# login is optional but gives access to more information
fac.login("201403027", "youWish")

# if no password is given, secret prompt will appear
fac.login("up201403027")
```

### Extract Student Information

```python
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
# the course url receives the id and the current school year,
# get_school_year returns the current school year, but could be hardcoded
mieic = fac.get_course((msramalho.courses[1].id, get_school_year()))

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

### Get All the Subjects of a Course
```python
# the study plan is identified by course id and occurrence year
# this will extract the information from the course study plan page
study_plan = fac.get_study_plan((mieic.study_plan.id, mieic.study_plan.year))

# to get all the information for all the optional subjects, for instance
# this will perform one request per subject
optionals = [fac.get_subject(s) for s in study_plan.optionals if s.code != ""]
```

### Get Subject Data and its Classes (all students for each class of that subject)
```python
# assuming we have a subject id (could be extracted from study_plan above)
plog = fac.get_subject(420002)

# get all the classes for this subject (needs course, school year and semester)
# if you miss some parameter you will see a message with all the parameters
# notice that it is ONLE ONE parameter, which is a tuple
subject_classes = fac.get_classes((mieic.id, plog.id, get_school_year(), plog.semester))

# now you can read all the students grouped by class
for c in subject_classes.classes:
    for student in c:
        print("Hello %s, your email is %s)" % (student.name, student.email))
# or simply list all the students in a given class (1st in this case (0 indexed))
print([s.name for s in classes.classes[0].students])
```

# Testing
Tests require a valid user account, to run them do:
```python
python -m unittest
```
And to get the coverage:
```python
coverage run -m unittest
coverage report --include="sigpy/*"
```
# Contributing
If you happen to use this tool you may need to extend the parsed parameters or add JSON classes or even extend it to new faculties, if you make them into pull-requests that would be awesome.

Also, if you just want to keep on building this tool, check the [contributing page](CONTRIBUTING.md)!