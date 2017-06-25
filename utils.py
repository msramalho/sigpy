import datetime

def getSchoolYear():
    now = datetime.datetime.now()
    if now.month <= 8:
        return now.year-1
    return now.year

def getIndent(indent):
    return " " * (2 * indent)

def constructStringVariable(indent, key = "", value = ""):
    base = getIndent(indent)
    base = (base + "%s%s" if key == "" else base + "%s: %s")
    if "classes" in str(type(value)):#this is an object
        return (base + "\n") % (key, constructString(value, indent + 1))
    else:
        return getIndent(indent + 1) + base % (key, str(value))

def constructString(obj, indent = -1):
    res = []
    for key, value in obj.__dict__.items():
        if value != "" and value != None:
            if type(value) == list and len(value) > 0:#list - iterate
                res.append("%s%s (%s)" % (getIndent(indent), key, str(len(value))))#line saying the number of elements
                for el in value:
                    res.append(constructStringVariable(indent+1, value=el))
                    res.append("")#paragraph
            else:
                res.append(constructStringVariable(indent, key, value))
    res[:] = [item for item in res if item != '']#remove empty elements
    return "\n".join(res)



#TODO:  function that removes all the expected but irrelevant html from a string to optimize regex search time and all that