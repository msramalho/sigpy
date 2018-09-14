import sys
sys.path.append('../')

from faculties.interface import *


class faculty(interface):
    interface.routes["base"] = "https://sigarra.up.pt/fmup/pt/"
    interface.routes["index"] = "https://sigarra.up.pt/fmup/pt/web_page.Inicial"
    interface.routes["student"] = "https://sigarra.up.pt/fmup/pt/fest_geral.cursos_list?pv_num_unico=%s"
    interface.routes["teacher"] = "https://sigarra.up.pt/fmup/pt/func_geral.formview?p_codigo=%s"
    interface.routes["teacher_schedule"] = "https://sigarra.up.pt/fmup/pt/hor_geral.docentes_view?pv_doc_codigo=%s"
    interface.routes["course"] = "https://sigarra.up.pt/fmup/pt/cur_geral.cur_view?pv_curso_id=%s&pv_ano_lectivo=%d"
    interface.routes["picture"] = "https://sigarra.up.pt/fmup/pt/fotografias_service.foto?pct_cod=%s"

    def __init__(self):
        super(faculty, self).__init__()
