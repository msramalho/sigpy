class person:
    def __init__(self, id="", name="unknown", emails = [], picture = None):
        self.id = id
        self.name = name
        self.emails = emails
        self.picture = picture

    def parse(self, html):
        print("PARSE Person")
        pass

    def __str__(self):
        return "ID%s - %s, emails:%s, picture=%s" % (self.id, self.name, tuple(self.emails), self.picture)
        