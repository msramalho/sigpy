from faculties.selector import getFaculty
from faculties.interface import interface

fac = getFaculty("feup")

#fac.findSubjects("https://sigarra.up.pt/feup/pt/cur_geral.cur_planos_estudos_view?pv_plano_id=2496&pv_ano_lectivo=2016&pv_tipo_cur_sigla=&pv_origem=CUR#div_id_285926")

i = interface("test")
i.startSession("up201403027")
exit()
#Test session start
print("Login: %s" % fac.startSession("up201403027"))


#Test find student

#fac.setLoad("loadCourses", True)
fac.setLoad("loadPictures", True)
mig = fac.findStudent("201403027")
mig.picture.show()

c = input("")
#Test find



