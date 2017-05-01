import sys
sys.path.append('../')
from faculties.interface import * 
from classes.student import *

class faculty(interface):
    def __init__(self, name):
        super(faculty, self).__init__(name)
        self.base = "https://sigarra.up.pt/feup/pt/"
        self.index = "https://sigarra.up.pt/feup/pt/web_page.Inicial"
        self.students = "https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=%s"
        self.courses = "https://sigarra.up.pt/feup/pt/cur_geral.cur_view?pv_curso_id=%s&pv_ano_lectivo=%d"

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
        req = self.session.get(self.students % id)
        parsed_html = BeautifulSoup(req.text, "html.parser")
        if parsed_html.body.find('form', attrs={'name':'voltar'}):#check if this id matches a student
            print("%s is not a valid id for a user at feup" % id)
            return None
        s = student(id)#assing id
        s.emails.append("up%s@fe.up.pt"%id)#add default email
        s.name = parsed_html.body.find('div', attrs={'class':'estudante-info-nome'}).text.strip()#read user's name
        #read active courses - estudante-lista-curso-activo
        activeCourses = parsed_html.body.find_all('div', attrs={'class':'estudante-lista-curso-activo'})
        for ac in activeCourses:
            c = courseStudent()
            nameHtml = ac.find('div', attrs={'class':'estudante-lista-curso-nome'})
            if nameHtml.a:
                p = re.compile(".*pv_curso_id=(\d+).*")
                c.id = p.findall(nameHtml.a.get("href"))[0]
                tempCourse = self.findCourse(c.id, nameHtml.a.get("href"))#try to get this course
                if tempCourse:#if it was successfully read
                    c.loadCourse(tempCourse)#update the courseStudent with all the details read
            c.name = nameHtml.text
            c.institution = ac.find('div', attrs={'class':'estudante-lista-curso-instit'}).text
            
            if self.checkSession():
                c.enrolled = ac.find("td", text="Ano da primeira inscrição:").find_next("td").text
                c.year = ac.find("td", text="Ano curricular atual:").find_next("td").text
                c.state = ac.find("td", text="Estado atual:").find_next("td").text
            
            s.courses.append(c)
        return s

    def findCourse(self, id, link = "", name = ""):#creates a course instance from the course id
        c = course(id = id)
        if link != "":#if the link for the course is passed, use it
            link = self.base + link
        else:#else use the id to generate the link
            link = self.courses % (id, getSchoolYear())

        req = self.session.get(link)#send get request

        if name =="":#if the name is not set, regex for it
            p = re.compile("<title>FEUP - (.+)<\/title>")
            name = p.findall(req.text)[0]
        c.name = name
        
        parsed_html = BeautifulSoup(req.text, "html.parser")

        #analyse table for info
        infoTableRows = parsed_html.body.find('table', attrs={'class':'formulario'}).find_all("tr")
        for row in infoTableRows:
            rowType = row.find(attrs={'class':'formulario-legenda'})
            rowValue = row.find(attrs={'class': None})
            if rowType.text == "Código Oficial: ":
                c.cod = rowValue.text
            elif rowType.text == "Diretor: ":
                c.director = rowValue.text
                #c.director = self.findTeacher(link=rowValue.a.get("href"))
            elif rowType.text == "Diretor Adjunto: ":
                c.directorAdj = rowValue.text
                #c.directorAdj = self.findTeacher(link=rowValue.a.get("href"))
            elif rowType.text == "Sigla: ":
                c.initials = rowValue.text
            elif rowType.text == "Grau Académico: ":
                c.degree = rowValue.text
            elif rowType.text == "Tipo de curso/ciclo de estudos: ":
                c.type = rowValue.text
            elif rowType.text == "Início: ":
                c.start = rowValue.text
            elif rowType.text == "Duração: ":
                c.duration = rowValue.text
                
        #get Subjects link
        c.subjectsLink = self.base + parsed_html.body.find('h3', text = "Planos de Estudos").findNext("div", attrs={"class":"caixa-informativa"}).findNext("li").a.get("href")
        return c
    def findTeacher(self, id, link ="", name=""):#sends get request for the teacher id and parses his/her information
        pass