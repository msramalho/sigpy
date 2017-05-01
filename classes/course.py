class course:
    def __init__(self, initials="", id="", cod="", name="", degree="", type="", start="", duration="", subjectsLink="", director="", directorAdj=""):
        self.name = name
        self.initials = initials
        self.id = id
        self.cod = cod
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
        return constructString(self)