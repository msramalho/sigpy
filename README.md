# Sigpy 🔨

[![Build Status](https://travis-ci.org/msramalho/sigpy.svg)](https://travis-ci.org/msramalho/sigpy)

This is a Sigarra Python API based on Recursive Web Scraping Parser (wtf). Essentially, it performs requests as needed (cached by default) and parses the html information into objects you can use.

The parser and interpreters are already there. All scrapping rules are specified in `.json` files that are automatically found, processed and magically made code-accessible, so if you extend it you barely have to do anything other than editing `.json` files!!

The concept behind this tool can be extended to other websites and one could ponder upon the interest of building something more general, like... "scraping for APIs"... _\*cough\*LDSO\*cough\*_

> In the end, this is yet another Sigarra-based project that I wished existed before I needed something like it.

# Demo

<p align="center"><img src="https://github.com/msramalho/sigpy/blob/master/examples/demo.gif?raw=true"/></p>

# Instalation
```bash
pip install git+https://github.com/msramalho/sigpy
```

# Examples
(Each example will hide all the code of the previous examples. The complete code can be found in [examples/main.py](examples/main.py))

For all the examples below, you need to start by importing sigpy:

```python
from sigpy import get_faculty, get_school_year
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

### Extract Teacher Information

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

# to get ALL the information for all the mandatory subjects
# they are grouped by year->semester->subjects
# this will perform one request per subject
mandatory = [fac.get_subject(s.id) for y in study_plan.years
                for sm in y.semesters for s in sm.subjects if s.code != ""]

# to get ALL the information for all the optional subjects, for instance
# this will perform one request per subject
optionals = [fac.get_subject(s.id) for s in study_plan.optionals if s.code != ""]
```

### Get Subject Data and its Classes (all students for each class of that subject)
```python
# assuming we have a subject id (could be extracted from study_plan above)
plog = fac.get_subject(420002)

# get all the classes for this subject (needs course, school year and semester)
# if you miss some parameter you will see a message correcting you,
# with all the values you need to give
# notice that it is ONLY ONE parameter, which is a (tuple)
subject_classes = fac.get_classes((mieic.id, plog.id, get_school_year(), plog.semester))

# now you can read all the students grouped by class
for c in subject_classes.classes:
    for student in c.students:
        print("Hello %s, your email is %s)" % (student.name, student.email))
# or simply list all the students in a given class (1st in this case (0 indexed))
print([s.name for s in classes.classes[0].students])
```

### Get a Subject's Timetable
```python
# this is actually an instance of the classes/timetable class
# this class can receive any html page with a timetable from sigarra and parses it
# this uses a python version of the SigTools parsing algorithm
# events are dicts which have a lot of attributes (from, to, name, room, ...)
plog_tt = fac.get_timetable(plog)

# to get a json view of the events
print(plog_tt)

# to get an array of the events for further use
plog_events = plog_tt.events
```

### Get Student Timetable (aka Stalker Mode)
The isolated code for this can be found in [examples/stalker.py](examples/stalker.py), but essentialy:
 * load the target student
 * get the courses of this student
 * for each course
     * get the study plan (ids of the subjects)
     * load every subject
     * get the classes (students in each class) for each subject
        * check if the target is in any of those classes
        * save the classes the target is in
     * produce a url to [TTS](https://ni.fe.up.pt/TTS) with the target's timetable

Alternatively, one could use the `fac.get_timetable(...)` to retrieve the custom times of the target's timetable, but since TTS made this script a step quicker, I just went for it.

This script will take some time the first time you run it for each course, after that cache makes it quite fast.

### Sky is the limit
This tool was built so there was a simple way to automate my endeavours into Sigarra, you can PR your own examples of tools into this section and help me and others get more out of sigpy.

## Cache
Since all of this is based on requests to Sigarra, and many requests are usually duplicates (and url's content rarely change), I have implemented a cache system that makes up for the time most requests take as, in time, most will be duplicates this can be very helpful (also if one of your scripts fails mid-execution).

Anyway, the cache is on by default. To turn it off for the current session:
```python
# this makes all the operations on fac produce requests
fac = get_faculty("feup", save_cache=False)

# if you just want to redo some requests (typically for dynamic pages), do
msr = fac.get_student("201403027", use_cache=False)
# this will not READ from cache, but it will UPDATE it
# (unless save_cache is False for the fac variable)
```
There is one cache file per faculty, inside the folder `%APPDATA%/sigpy/cache/"FACULTY"/_cache.json`. You can open and edit it maually as it is a JSON mapping of a python dict (url->html), you can also delete it manually and programatically, as follows:
```python
# this will remove the file on disk for the current faculty only
fac.cache.delete()
```

Note: Pictures are not cached, only html content. This html is minify but further work can be made into cleaning it further (for instance removing inline scripts, ...)

## Verbosity
By default, no print is done, to enable warnings about atributes that were not found in the parsed pages, do:
```python
# obviously, this can be toggled with either True or False
fac.set_verbose(True) # default False
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
And to get the html report:
```python
coverage run -m unittest
coverage html --include="sigpy/*"
```

# Contributing
If you happen to use this tool you may need to extend the parsed parameters or add JSON classes or even extend it to new faculties, if you make them into pull-requests that would be awesome.

Also, if you just want to keep on building this tool, check the [contributing page](CONTRIBUTING.md)!
