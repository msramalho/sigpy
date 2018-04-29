from faculties.selector import get_faculty
from faculties.interface import interface


#fac.findSubjects("https://sigarra.up.pt/feup/pt/cur_geral.cur_planos_estudos_view?pv_plano_id=2496&pv_ano_lectivo=2016&pv_tipo_cur_sigla=&pv_origem=CUR#div_id_285926")

# load FEUP
fac = get_faculty("feup")

# Login into sigarra
p = "TODO"
print("Login: %s" % fac.login("up201403027", p))

# get a student
me = fac.get_student("201403027")
print(me)

# get a student picture and display it
# fac.get_picture(me.id).show()
