import unittest
from sigpy import get_faculty, get_school_year


class test_feup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fac = get_faculty("feup")

    def test_get(self):
        self.course = self.fac.get_course((742, get_school_year()))
        self.assertEqual(self.course.name, "Mestrado Integrado em Engenharia Informática e Computação")
        self.assertEqual(self.course.cod, "9459")
        self.assertEqual(self.course.id, (742, get_school_year()))
        self.assertIsNotNone(self.course.director)
        self.assertIsNotNone(self.course.assistant_director)
