from sigpy import get_faculty

# fac.findSubjects("https://sigarra.up.pt/feup/pt/cur_geral.cur_planos_estudos_view?pv_plano_id=2496&pv_ano_lectivo=2016&pv_tipo_cur_sigla=&pv_origem=CUR#div_id_285926")

# load FEUP
fac = get_faculty("feup")

# Login into sigarra
p = ""

print("Login: %s" % fac.login("up201403027", p))

# access student data!
msr = fac.get_student("UP201403027") # up is case insensitive and also unnecessary
# print(msr) # complete JSON view of student information

# access course data!
mieic = fac.get_course(msr.courses[1].id) # pass the id of msr's second course (which is MIEIC)
# print(mieic)

# access teacher data!
pascoal = fac.get_teacher(mieic.director.id) # use the id of the course director

fotogenico = fac.get_picture(pascoal)
fotogenico.save("C:/Users/M/Desktop/")

# get a student
# me = fac.get_student("201303462") # mota

# fac.get_course(me.courses, filter=lambda c: c.id != null)
# mieic = fac.get_course(me.courses[1].id)
# print(mieic)

# mieic = fac.get_course(me.courses[1].id, me.courses[1])
# print(mieic)

# miem = fac.get_course(743)
# print(miem)


# get a student picture and display it
# fac.get_picture(fac.get_student("201403090")).show()

# get a teacher
# pascoal = fac.get_teacher(mieic.director.id)
# print(pascoal)
# fac.get_picture(pascoal).show()
# p_room = fac.get_room(pascoal.rooms[0].id)
# print(p_room)
# fac.get_picture(p_room).show()
