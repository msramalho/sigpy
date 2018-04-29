import sys, shutil
sys.path.append('../')
from faculties.interface import *
class faculty(interface):
    name = "fmup"

    interface.routes["base"] = "https://sigarra.up.pt/fmup/pt/"
    interface.routes["index"] = "https://sigarra.up.pt/fmup/pt/web_page.Inicial"
    interface.routes["student"] = "https://sigarra.up.pt/fmup/pt/fest_geral.cursos_list?pv_num_unico=%s"
    interface.routes["teacher"] = "https://sigarra.up.pt/fmup/pt/func_geral.formview?p_codigo=%s"
    interface.routes["teacher_schedule"] = "https://sigarra.up.pt/fmup/pt/hor_geral.docentes_view?pv_doc_codigo=%s"
    interface.routes["course"] = "https://sigarra.up.pt/fmup/pt/cur_geral.cur_view?pv_curso_id=%s&pv_ano_lectivo=%d"
    interface.routes["picture"] = "https://sigarra.up.pt/fmup/pt/fotografias_service.foto?pct_cod=%s"

    def __init__(self):
        super(faculty, self).__init__()

    def completeCourse(self, c, nameHtml):#(done) avoid duplicate code
        p = re.compile(".*pv_curso_id=(\d+).*")
        c.id = p.findall(nameHtml.a.get("href"))[0]
        tempCourse = self.findCourse(c.id)#try to get this course
        if tempCourse:#if it was successfully read
            c.loadCourse(tempCourse)#update the courseStudent with all the details read
        return c

    def findStudent(self, id):#(done)sends get request for the student id and parses his/her information, if loadCourses is false only the name of the course will be loaded and not the other details, if loadTeachers is True the director of the courses will be loaded (if, of course, loadCourses is True)
        req = self.session.get(self.students % id)
        parsed_html = BeautifulSoup(req.text, "html.parser")
        if parsed_html.body.find('form', attrs={'name':'voltar'}):#check if this id matches a student
            print("%s is not a valid id for a student at fmup" % id)
            return None
        #create and populate student instance
        s = student(id)#assing id
        s.emails.append("up%s@fe.up.pt"%id)#add default email
        s.name = parsed_html.body.find('div', attrs={'class':'estudante-info-nome'}).text.strip()#read user's name
        #read active courses for this student
        activeCourses = parsed_html.body.find_all('div', attrs={'class':'estudante-lista-curso-activo'})
        for ac in activeCourses:
            c = courseStudent()
            nameHtml = ac.find('div', attrs={'class':'estudante-lista-curso-nome'})
            if self.loadCourses and nameHtml.a:#if this has a link
                c = self.completeCourse(c, nameHtml)
            c.name = nameHtml.text
            c.institution = ac.find('div', attrs={'class':'estudante-lista-curso-instit'}).text
            #get attributes that require session
            if self.checkSession():
                c.enrolled = ac.find("td", text="Ano da primeira inscrição:").find_next("td").text
                #c.year = ac.find("td", text="Ano curricular atual:").find_next("td").text
                #c.state = ac.find("td", text="Estado atual:").find_next("td").text

            s.courses.append(c)
        #read inactive courses for this student
        inactiveCourses = parsed_html.body.find_all('div', attrs={'class':'tabela-longa'})
        for ic in inactiveCourses:
            c = courseStudent()
            nameHtml = ic.find('td', attrs={'class':['t','k']})
            if self.loadCourses and nameHtml.a:#if this has a link
                c = self.completeCourse(c, nameHtml)
            c.name = nameHtml.text
            tableRows = ic.find('tr', attrs={'class':'i'}).find_all("td")
            c.institution = tableRows[1].a["title"]
            if self.checkSession():
                c.enrolled = tableRows[4].text
                c.state = tableRows[5].text
            s.courses.append(c)
        if self.loadPictures:
            print("Geting picture...")
            s.picture = self.getPicture(s.id)
        return s

    def findCourse(self, id, link = "", name = ""):#(done)creates a course instance from the course id
        print("Link(%s): %s" % (id, link))
        c = course(id = id)
        if link != "":#if the link for the course is passed, use it
            link = self.base + link
        else:#else use the id to generate the link
            link = self.courses % (id, getSchoolYear())

        req = self.session.get(link)#send get request

        if name =="":#if the name is not set, regex for it
            p = re.compile("<title>fmup - (.+)<\/title>")
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
            elif rowType.text == "Diretor: " and self.loadTeachers:#find if loadTeachers is True
                p = re.compile("pct_codigo=(.+)")#get the id from the regex
                teacherId = p.findall(rowValue.a.get("href"))[0]
                c.director = self.findTeacher(teacherId)
            elif rowType.text == "Diretor Adjunto: " and self.loadTeachers:#find loadTeachers is True
                p = re.compile("pct_codigo=(.+)")#get the id from the regex
                teacherId = p.findall(rowValue.a.get("href"))[0]
                c.directorAdj = self.findTeacher(teacherId)
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
    def findTeacher(self, id, link ="", name=""):#(done)sends get request for the teacher id and parses his/her information
        req = self.session.get(self.teachers % id)
        parsed_html = BeautifulSoup(req.text, "html.parser")
        if parsed_html.body.find('form', attrs={'name':'voltar'}):#check if this id matches a student
            print("%s is not a valid id for a teacher at fmup" % id)
            return None
        t = teacher(id)
        t.emails = []
        t.positions = []
        teacherDetails = parsed_html.body.find_all('td', attrs={'class':'formulario-legenda'})
        for detail in teacherDetails:
            if detail.text == "Nome:":
                t.name = detail.find_next("td").text.strip()
                websiteFind = parsed_html.body.find("a", attrs={"title":"Ligação à página pessoal de %s" % t.name})
                t.website = websiteFind.get("href") if websiteFind else ""
            elif detail.text == "Sigla:":
                t.initials = detail.find_next("td").text
            #elif detail.text == "Código:": #we already have this
                #t.id = detail.find_next("td").text
            elif detail.text == "Estado:":
                t.status = detail.find_next("td").text
            elif detail.find("img", attrs={"title":"ORCID"}):#orcid link
                p = re.compile("http://orcid.org/(.+)")#get the id from the regex
                t.orcid = p.findall(detail.find_next("td").text)[0]
            elif detail.text == "Salas: ":
                rooms = detail.find_all("a")
                p = re.compile("instal_geral.espaco_view?pv_id=(.+)")#get the id from the regex
                for room in rooms:#iterate all the rooms
                    roomId = p.findall(room.get("href"))[0]
                    t.rooms.append(self.getRoom(roomId, room.name))
            elif detail.text == "Categoria:":
                t.category = detail.find_next("td").text
            elif detail.text == "Carreira:":
                t.career = detail.find_next("td").text
            elif detail.text == "Departamento:":
                t.department = detail.find_next("td").text
            elif detail.text == "Secção:":
                t.section = detail.find_next("td").text
            elif detail.text == "Voip:":
                t.voip = detail.find_next("td").text
            elif detail.text == "Email Institucional:" or detail.text == "Email alternativo:" :
                detail.find_next("td").find("img").wrap(parsed_html.new_tag("div")).insert_before("@") #add the @ to get the full email in the next step
                t.emails.append(detail.find_next("td").text)
            #elif detail.text == "_________":
                #t.name = detail.find_next("td").text
        teacherDetails = parsed_html.body.find_all('tr', attrs={'class':'k d'})
        for detail in teacherDetails:
            t.positions.append((detail.find_next("td", attrs={"class":"k"}).text + " " + detail.find_next("td", attrs={"class":"l"}).text).strip())
        #get schedule: teachersSchedule
        return t
    def findRoom(self, id, name = ""):#creates a room instance from the room id
        print("ROOM %s - id: %s" % (name, id))
    def findSubject(self, id):#creates a subject instance from the subject id
        print(notImplementedWarning % self.name)
    def findSubjects(self, url):#returns a list of subjects in a url
        req = self.session.get(url)
        parsed_html = BeautifulSoup(req.text, "html.parser")
        if parsed_html.body.find('form', attrs={'name':'voltar'}):#check if this id matches a student
            print("%s is not a valid link for subjects at fmup" % id)
            return None
        subjectLink = parsed_html.body.find_all('a', attrs={'href':re.compile('ucurr_geral\.ficha_uc_view\?pv_ocorrencia_id=.*')})
        print("FOUND: %d subjects" % len(subjectLink))


    def getPicture(self, id, path = "", display = False, save = True):#reads the picture from the web and returns it, if it exists
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        r = self.session.get(self.pictures%str(id), stream=True, headers=headers)
        if not path:
            path = self.picturesFolder
        path += "%s.jpg" % str(id)
        result = False
        print(self.pictures%str(id))
        print(r)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            result = picture(os.path.abspath(path))
            if display:
                result.show()
            if not save:
                result.delete()
        return result