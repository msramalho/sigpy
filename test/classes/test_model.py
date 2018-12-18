import unittest
from sigpy.classes import model


model_name = "test_model"
original = {"int": 10, "char": 'a', "string": "ab de", "list": [None, 0, 1, "a", []]}
model_dict = original
model_dict['class_name'] = model_name


class SigTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.m = model(model_name, original)

    def test_init(self):
        self.assertEqual(self.m.class_name, "test_model")
        self.assertEqual(self.m.int, 10)
        self.assertEqual(self.m.char, 'a')
        self.assertEqual(self.m.string, "ab de")
        self.assertEqual(self.m.list, [None, 0, 1, "a", []])

    def test_json(self):
        self.assertIsNotNone(self.m.json)
        self.assertDictEqual(self.m.json(), model_dict)

    def test_str(self):
        self.assertIsNotNone(self.m.__str__)
        self.assertEqual(len(str(self.m)), 138, "should be json with identation 2")

    def test_repr(self):
        self.assertIsNotNone(self.m.__repr__)
        self.assertEqual(len(str([self.m])), 140, "should be json with identation 2 and __repr__ should be implemented")

    def test_get_item(self):
        self.assertIsNotNone(self.m.__getitem__)
        self.assertEqual(self.m["class_name"], "test_model")
        self.assertEqual(self.m["int"], 10)
        self.assertEqual(self.m["char"], 'a')
        self.assertEqual(self.m["string"], "ab de")
        self.assertEqual(self.m["list"], [None, 0, 1, "a", []])

    def test_iter(self):
        self.assertIsNotNone(self.m.__iter__)
        for k, v in self.m:
            self.assertEqual(v,original[k])

    def test_inner_clases(self):
        class temp:
            def __init__(self, a, b):
                self.a, self.b = a, b
        self.m2 = model("model_with_inner", {"inner": self.m, "other_class": temp(-1, 20)})
        self.assertEqual(len(self.m2.json()), 3)

if __name__ == "__main__":
    unittest.main()
