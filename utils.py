import time
import uuid
import os.path

tokens = set()


def log(*args, **kwargs):
	print(*args, **kwargs)


def get_local_time(time_seconds):
	t = time.localtime(time_seconds)
	return time.strftime("%Y-%m-%d %H:%M:%S", t)


def generate_token():
	token = str(uuid.uuid4())
	tokens.add(token)
	return token


def encrypt(pwd):
	from app import app
	from hashlib import md5
	key = app.secret_key + pwd
	return md5(key.encode("ascii")).hexdigest()


def init_db():
	if not os.path.exists("db"):
		os.mkdir("db")
	classes = ["User", "Topic", "Reply", "Board"]
	for c in classes:
		db_path = "db{}{}.json".format(os.sep, c)
		if not os.path.exists(db_path):
			with open(db_path, "w", encoding="utf-8") as f:
				f.write("[]")

