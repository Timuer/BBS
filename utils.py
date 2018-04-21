import time

def log(*args, **kwargs):
	print(*args, **kwargs)


def get_local_time(time_seconds):
	t = time.localtime(time_seconds)
	return time.strftime("%Y-%m-%d %H:%M:%S", t)