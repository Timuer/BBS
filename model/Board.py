from model import Model


class Board(Model):
	def __init__(self, form):
		self.id = form.get("id", "")
		self.title = form.get("title", "")
		self.description = form.get("description", "")