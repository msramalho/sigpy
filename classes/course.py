class course:
    def __init__(self, intials="", id="", cod="", name="", director="", directorAdj="", degree="", type="", start="", duration="", subjectsLink=""):
        self.initials = intials
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
