from model import MongoModel
from model.User import User
from model.Board import Board
import time

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
		board_id = form.get("board_id")
		m.board = Board.find_by_id(board_id).title
		m.save()
		return m

	def calc_time(self):
		ct = self.created_time
		nt = int(time.time())
		time_past = nt - ct
		ONE_YEAR = 60 * 60 * 24 * 365
		ONE_MONTH = 60 * 60 * 24 * 30
		ONE_DAY = 60 * 60 * 24
		ONE_HOUR = 60 * 60
		ONE_MINUTE = 60
		if time_past > ONE_YEAR:
			return "{}年前".format(int(time_past/ONE_YEAR))
		elif time_past > ONE_MONTH:
			return "{}月前".format(int(time_past/ONE_MONTH))
		elif time_past > ONE_DAY:
			return "{}天前".format(int(time_past/ONE_DAY))
		elif time_past > ONE_HOUR:
			return "{}小时前".format(int(time_past/ONE_HOUR))
		elif time_past > ONE_MINUTE:
			return "{}分钟前".format(int(time_past/ONE_MINUTE))
		else:
			return "刚刚"





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
