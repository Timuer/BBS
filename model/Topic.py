from model import MongoModel
from model.User import User

class Topic(MongoModel):
	__fields__ = MongoModel.__fields__ + [
		("title", str, ""),
		("board", str, ""),
		("username", str, ""),
		("views", int, 0),
		("comments", int, 0),
		("user_id", int, -1),
		("content", str, ""),
		("board_id", int, -1),
	]

	@classmethod
	def new_and_save(cls, form=None, **kwargs):
		m = cls.new(form, **kwargs)
		user_id = form.get("user_id")
		user = User.find_by_id(int(user_id))
		m.username = user.username
		m.save()
		return m




"""
class Topic(Model):
	def __init__(self, form):
		self.id = form.get("id", "")
		self.title = form.get("title", "")
		self.board = form.get("board", "")
		self.username = form.get("username", "")
		self.views = form.get("views", 0)
		self.comments = form.get("comments", 0)
		self.user_id = form.get("user_id", "")
		self.content = form.get("content", "")
		self.board_id = form.get("board_id", "")

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
