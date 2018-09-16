from sigpy.interface import interface
from sigpy.utils import getSchoolYear


class faculty(interface):
    interface.routes["base"] = "https://sigarra.up.pt/feup/pt/"
    interface.routes["index"] = "https://sigarra.up.pt/feup/pt/web_page.Inicial"
    interface.routes["student"] = "https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=%s"
    interface.routes["teacher"] = "https://sigarra.up.pt/feup/pt/func_geral.formview?p_codigo=%s"
    interface.routes["teacher_schedule"] = "https://sigarra.up.pt/feup/pt/hor_geral.docentes_view?pv_doc_codigo=%s"
    interface.routes["course"] = "https://sigarra.up.pt/feup/pt/cur_geral.cur_view?pv_curso_id=%s&pv_ano_lectivo=%d" % ("%s", getSchoolYear())
    interface.routes["study_plan"] = "https://sigarra.up.pt/feup/pt/cur_geral.cur_planos_estudos_view?pv_plano_id=%s&pv_ano_lectivo=%s&pv_tipo_cur_sigla=&pv_origem=CUR"
    interface.routes["subject"] = "https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=%s"
    interface.routes["picture"] = "https://sigarra.up.pt/feup/pt/fotografias_service.foto?pct_cod=%s"
    interface.routes["room"] = "https://sigarra.up.pt/feup/pt/instal_geral.espaco_view?pv_id=%s"
    interface.routes["room_picture"] = "https://sigarra.up.pt/feup/pt/instal_geral2.get_mapa?pv_id=%s"

    def __init__(self):
        super(faculty, self).__init__()