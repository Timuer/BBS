from model import Model

class User(Model):
	def __init__(self, form):
		self.id = form.get("id", "")
		self.username = form.get("username", "")
		self.password = form.get("password", "")
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
		username = form.get("username")
		users = cls.all()
		if username in (u.username for u in users):
			return False, "用户已存在"
		User.new(form)
		return True, ""

