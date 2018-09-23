
from sigpy import get_faculty, get_school_year

### Login to your account

# get faculty object and login
fac = get_faculty("feup")

# login is optional but gives access to more information
fac.login("201403027", "YOUR_PASSWORD_HERE_OR_JUST_USE_PROMPT_VERSION_BY_REMOVING_PARAMETER")

### Extract Student Information

# access student data from their id
# "up" is case insensitive and also optional
msramalho = fac.get_student("UP201403027")

# print a complete JSON view of student information
print(msramalho)

# or simply use the attribute you need
# a complete list is available in the JSON view
message = "Nice to meet you, %s" % msramalho.name

### Access Course Data

# load mieic from the student (we know it is at index 1)
# the course url receives the id and the current school year,
# get_school_year returns the current school year, but could be hardcoded
mieic = fac.get_course((msramalho.courses[1].id, get_school_year()))

# print a complete JSON view of course information
print(mieic)

### Extract Teacher Information

# use the id of the course director to access teacher data!
# (the name of the variable may lose meaning in the future)
pascoal = fac.get_teacher(mieic.director.id)

# print a complete JSON view of teacher information
print(pascoal)

### Get Student, Teacher and Room Pictures
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

# and even for room layout pictures
room = fac.get_room(vidal.rooms[0].id)
fac.get_picture(room).show()

### Get All the Subjects of a Course
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

### Get Subject Data and its Classes (all students for each class of that subject)
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

### Get a Subject's Timetable
# this is actually an instance of the classes/timetable class
# this class can receive any html page with a timetable from sigarra and parse it
plog_tt = fac.get_timetable(plog)

# to parse the events (aka subject's classes) from the html
# this uses a python version of the SigTools parsing algorithm
# events are dicts which have a lot of attributes (from, to, name, room, ...)
plog_events = plog_tt.get_events()
