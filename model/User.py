from model import Model

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
		username = form.get("username", "")
		email = form.get("email", "")
		users = cls.all()
		if username in (u.username for u in users):
			return False, "用户已存在"
		if not validate_email(email):
			return False, "邮箱格式错误"
		User.new(form)
		return True, ""


def validate_email(email):
	pass

