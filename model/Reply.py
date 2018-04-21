from model import Model
from model.User import User


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