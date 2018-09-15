import json

class JsonClassEncoder(json.JSONEncoder):
	# needed to print classes inside other classes (that inherit from model) using json.dumps
    def default(self, obj):
        if hasattr(obj,'json'):
            return obj.json()
        else:
            return json.JSONEncoder.default(self, obj)


class model:
	def __init__(self, name, dictionary):
		self.class_name = name
		for k, v in dictionary.items():
			setattr(self, k, v)

	def json(self):
		return self.__dict__

	def __str__(self):
		return json.dumps(self.__dict__, ensure_ascii=False, cls=JsonClassEncoder, indent=2)

	def __repr__(self):
		return self.__str__
