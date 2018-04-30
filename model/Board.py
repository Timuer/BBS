from model import MongoModel

class Board(MongoModel):
	__fields__ = MongoModel.__fields__ + [
		("title", str, ""),
		("description", str, ""),
	]



"""
class Board(Model):
	def __init__(self, form):
		self.id = form.get("id", "")
		self.title = form.get("title", "")
		self.description = form.get("description", "")
"""