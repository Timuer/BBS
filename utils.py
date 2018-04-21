import time
import uuid

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