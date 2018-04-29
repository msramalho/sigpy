import sys
import os.path
import importlib
sys.path.append('../')


def get_faculty(faculty="feup"):
    if not os.path.isfile("faculties/%s.py" % faculty):  # not supported
        print("The faculty %s has no file to import" % faculty)
        exit(1)
    mod = importlib.import_module("faculties.%s" % faculty)  # import the correct file
    return mod.faculty()
