from pymongo import MongoClient
import time

db = MongoClient("localhost", 27017).bbs


class MongoModel(object):
	__fields__ = [
		("id", int, 0),
		("created_time", int, -1),
		("updated_time", int, -1),
		("deleted", bool, False),
	]

	@classmethod
	def doc(cls):
		return db[cls.__name__]

	@classmethod
	def next_id(cls):
		# 创建 data_id 文档集合
		data_id = db["data_id"]
		# 第三个参数表示不存在则创建（upsert）
		data_id.update({"model":cls.__name__}, {"$inc": {"count": 1}}, True)
		return data_id.find_one({"model":cls.__name__})["count"]

	"""
		用于外部调用，从表单生成一个映射的模型对象
	"""

	@classmethod
	def new(cls, form=None, **kwargs):
		model = cls()
		fields = cls.__fields__.copy()
		if form is None:
			form = {}
		for key, tp, value in fields:
			if key in form:
				setattr(model, key, tp(form[key]))
			else:
				setattr(model, key, value)
		for k, v in kwargs:
			if hasattr(model, k):
				setattr(model, k, v)
			else:
				raise KeyError
		setattr(model, "created_time", int(time.time()))
		setattr(model, "updated_time", int(time.time()))
		setattr(model, "id", cls.next_id())
		return model

	@classmethod
	def new_and_save(cls, form=None, **kwargs):
		m = cls.new(form, **kwargs)
		m.save()
		return m

	"""
		用于模型内部调用，从Mongo数据库中查询到的bson格式
		数据恢复成模型对象
	"""

	@classmethod
	def _new_from_mongo(cls, bson):
		model = cls()
		fields = cls.__fields__.copy()
		for key, tp, value in fields:
			if key in bson:
				setattr(model, key, bson[key])
			else:
				setattr(model, key, value)
		setattr(model, "_id", bson["_id"])
		return model

	@classmethod
	def _find(self, sort_key=None, **kwargs):
		kwargs["deleted"] = False
		if sort_key:
			lst = list(self.doc().find(kwargs).sort(sort_key))
		else:
			lst = list(self.doc().find(kwargs))
		return lst

	@classmethod
	def all(cls):
		ms = cls._find()
		return [cls._new_from_mongo(m) for m in ms]

	@classmethod
	def find_by(cls, **kwargs):
		ms = cls._find(sort_key=None, **kwargs)
		return [cls._new_from_mongo(m) for m in ms]

	@classmethod
	def find_by_id(cls, id):
		id = int(id)
		m = cls.doc().find_one({"id": id})
		return cls._new_from_mongo(m)

	@classmethod
	def delete(cls, id):
		cls.doc().update({"id":id}, {"$set":{"deleted":True}})

	def save(self):
		self.doc().save(self.__dict__)

	def update(self):
		d = self.__dict__
		_id = d.pop("_id")
		self.doc().update({"_id": _id}, {"$set": d})



"""
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
"""


