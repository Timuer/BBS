from model import Model
from flask import session
from utils import tokens


class User(Model):
	def __init__(self, form):
		self.id = form.get("id", "")
		self.username = form.get("username", "")
		self.password = form.get("password", "")
		self.email = form.get("email", "")
		self.description = form.get("description", "")

	@classmethod
	def validate_login(cls, form):
		users = cls.all()
		for u in users:
			if u.username == form.get("username") and u.password == form.get("password"):
				return u
		return None

	@classmethod
	def register(cls, form):
		token = form.get("_xsrf", "")
		if token not in tokens:
			return False, "请不要重复提交表单"
		else:
			tokens.pop(token)
		username = form.get("username", "")
		users = cls.all()
		if username in (u.username for u in users):
			return False, "用户已存在"
		User.new(form)
		return True, ""


def current_user():
	user_id = session.get("user_id", None)
	if user_id:
		return User.find_by_id(user_id)
	else:
		return None


def validate_email(email):
	pass
