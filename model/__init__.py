import json
import uuid
import os


def load(path):
	with open(path, "r", encoding="utf-8") as f:
		s = f.read()
		return json.loads(s)


def save(path, data):
	s = json.dumps(data, ensure_ascii=False, indent=2)
	with open(path, "w", encoding="utf-8") as f:
		f.write(s)


class Model(object):
	@classmethod
	def getid(cls):
		return str(uuid.uuid4())

	@classmethod
	def model_path(cls):
		name = cls.__name__
		path = "db{}{}.json".format(os.sep, name)
		return path

	@classmethod
	def new(cls, form):
		model = cls(form)
		model.id = cls.getid()
		model.save()
		return model

	@classmethod
	def _new_from_dict(cls, d):
		o = cls({})
		for k, v in d.items():
			setattr(o, k, v)
		return o

	@classmethod
	def all(cls):
		path = cls.model_path()
		dicts = load(path)
		return [cls._new_from_dict(d) for d in dicts]

	@classmethod
	def find_by(cls, **kwargs):
		models = cls.all()
		result_set = []
		for m in models:
			if cls._match(m, kwargs):
				result_set.append(m)
		return result_set

	@classmethod
	def find_by_id(cls, id):
		models = cls.all()
		for m in models:
			if m.id == id:
				return m

	@classmethod
	def _match(cls, model, kwargs):
		flag = True
		for k, v in kwargs.items():
			if model.__dict__.get(k) != v:
				flag = False
		return flag

	@classmethod
	def delete(cls, id):
		path = cls.model_path()
		models = cls.all()
		index = -1
		for i, m in enumerate(models):
			if m.id == id:
				index = i
		if index != -1:
			del models[index]
			model_list = [m.__dict__ for m in models]
			save(path, model_list)

	def save(self):
		path = self.model_path()
		models = self.all()
		models.append(self)
		model_list = [m.__dict__ for m in models]
		save(path, model_list)

	def update(self):
		id = self.id
		self.delete(id)
		self.save()

	def json(self):
		return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

	def __repr__(self):
		classname = self.__class__.__name__
		properties = ["{}: ({})".format(k, v) for k, v in self.__dict__.items()]
		s = "\n".join(properties)
		return "< {}\n{} >\n".format(classname, s)
