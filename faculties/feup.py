import sys
sys.path.append('../')
from faculties.interface import * 
from classes.student import *
class faculty(interface):
    def __init__(self, name):
        super(faculty, self).__init__(name)
        self.index = "https://sigarra.up.pt/feup/pt/web_page.Inicial"
        self.students = "https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=%s"

    def __str__(self):
        return "THIS IS FEUP"

    def startSession(self, username, password):#creates a requests session to access protecte pages
        self.session = requests.Session()
        payload = {'p_user': username, 'p_pass': password}
        r = self.session.post('https://sigarra.up.pt/feup/pt/vld_validacao.validacao', params=payload)
        if re.search("O conjunto utilizador/senha não é válido.", r.text):
            self.session = None
            return False
        return True

    def findStudent(self, id, loadCourses = True):#sends get request for the student id and parses his/her information, is loadCourses is false only the name of the course will be loaded and not the other details
        req = requests.get(self.students % id)
        parsed_html = BeautifulSoup(req.text, "html.parser")
        if parsed_html.body.find('form', attrs={'name':'voltar'}):#check if this id matches a student
            print("%s is not a valid id for a user at feup" % id)
            return None
        s = student(id)#assing id
        s.emails.append("up%s@fe.up.pt"%id)#add default email
        s.name = parsed_html.body.find('div', attrs={'class':'estudante-info-nome'}).text.strip()#read user's name
        #read active courses - estudante-lista-curso-activo
        activeCourses = parsed_html.body.find_all('div', attrs={'class':'estudante-lista-curso-activo'})
        for c in activeCourses:
            print(c.find('div', attrs={'class':'estudante-lista-curso-nome'}).text)
        return s

    def findCourse(self, id):#creates a course instance from the course id
        pass
        
        