import datetime
def getSchoolYear():
    now = datetime.datetime.now()
    if now.month <= 8:
        return now.year-1
    return now.year


#TODO:  function that removes all the expected but irrelevant html from a string to optimize regex search time and all that