from model import MongoModel
from model.User import User

class Reply(MongoModel):
	__fields__ = MongoModel.__fields__ + [
		("user_id", int, -1),
		("topic_id", int, -1),
		("username", str, ""),
		("floor", int, 0),
		("likes", int, 0),
		("like_users", list, []),
		("content", str, ""),
	]

	@classmethod
	def new_and_save(cls, form=None, **kwargs):
		m = cls.new(form, **kwargs)
		user_id = form.get("user_id")
		user = User.find_by_id(user_id)
		m.username = user.username
		m.save()
		return m


"""
class Reply(Model):
	def __init__(self, form):
		self.user_id = form.get("user_id", "")
		self.topic_id = form.get("topic_id", "")
		self.username = form.get("username", "")
		self.floor = int(form.get("floor", 0))
		self.likes = form.get("likes", 0)
		self.like_users = []
		self.content = form.get("content", "")

	@classmethod
	def new(cls, form):
		m = cls(form)
		m.id = cls.getid()
		user_id = form.get("user_id")
		user = User.find_by_id(user_id)
		m.user_id = user_id
		m.username = user.username
		m.save()
"""