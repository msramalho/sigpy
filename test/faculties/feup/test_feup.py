import unittest
from sigpy import get_faculty, get_school_year


class SigTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fac = get_faculty("feup")
        self.fac.login("201403027")

    def test_get_course(self):
        course = self.fac.get_course((742, get_school_year()))
        self.assertEqual(course.name, "Mestrado Integrado em Engenharia Informática e Computação")
        self.assertEqual(course.cod, "9459")
        self.assertEqual(course.id, (742, get_school_year()))
        self.assertIsNotNone(course.director)
        self.assertIsNotNone(course.assistant_director)

    def test_get_teacher(self):
        pascoal = self.fac.get_teacher(210006)
        self.assertEqual(pascoal.name, "João Carlos Pascoal Faria")
        self.assertEqual(pascoal.initials, "JPF")
        self.assertEqual(pascoal.orcid, "0000-0003-3825-3954")
        self.assertEqual(pascoal.phone, "225081316")
        self.assertEqual(pascoal.voip, "3386")
        self.assertEqual(pascoal.email, "jpf@fe.up.pt")


if __name__ == "__main__":
    unittest.main()
