class course:
    def __init__(self, initials="", id="", cod="", name="", director="", directorAdj="", degree="", type="", start="", duration="", subjectsLink=""):
        self.initials = initials
        self.id = id
        self.cod = cod
        self.name = name
        self.director = director
        self.directorAdj = directorAdj
        self.degree = degree
        self.type = type
        self.start = start
        self.duration = duration
        self.subjectsLink = subjectsLink
    
    def parse(self, html):
        pass

    def __str__(self):
        return "Course %s: %s (%s)\nDirector:%s\nDirector Adj:%s\nDegree:%s\nType:%s\nStart:%s\nDuration:%s"% (self.id, self.name, self.cod, self.director, self.directorAdj, self.degree, self.type, self.start, self.duration)