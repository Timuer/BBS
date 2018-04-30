from model import MongoModel
from flask import session
from utils import tokens
from utils import encrypt

class User(MongoModel):
	__fields__ = MongoModel.__fields__ + [
		("sex", str, ""),
		("image", str, ""),
		("username", str, ""),
		("password", str, ""),
		("email", str, ""),
		("description", str, ""),
	]

	@classmethod
	def new_and_save(cls, form=None, **kwargs):
		m = cls.new(form, **kwargs)
		pwd = m.password
		m.password = encrypt(pwd)
		m.save()

	@classmethod
	def validate_login(cls, form):
		users = cls.all()
		for u in users:
			if u.username == form.get("username") and u.password == encrypt(form.get("password")):
				return u
		return None

	@classmethod
	def register(cls, form):
		token = form.get("_xsrf", "")
		if token not in tokens:
			return False, "请不要重复提交表单"
		else:
			tokens.remove(token)
		username = form.get("username", "")
		users = cls.all()
		if username in (u.username for u in users):
			return False, "用户已存在"
		cls.new_and_save(form)
		return True, ""


def current_user():
	user_id = session.get("user_id", None)
	if user_id:
		return User.find_by_id(user_id)
	else:
		return None


""""

class User(Model):
	def __init__(self, form):
		self.id = form.get("id", "")
		self.sex = form.get("sex", "")
		self.image = form.get("image", "")
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
			tokens.remove(token)
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
	
"""
