from flask import (
	Blueprint,
	request,
	redirect,
	url_for,
)
from model.Reply import Reply
from model.Topic import Topic
from model.User import current_user

reply_routes = Blueprint("reply", __name__)


@reply_routes.route("/add/<topic_id>", methods=["POST"])
def add(topic_id):
	u = current_user()
	if not u:
		return redirect(url_for("auth.login"))
	Reply.new(request.form)
	t = Topic.find_by_id(topic_id)
	update_comments(t)
	return redirect(url_for("topic.detail", topic_id=topic_id))


@reply_routes.route("/votes/<reply_id>")
def votes(reply_id):
	u = current_user()
	r = Reply.find_by_id(reply_id)
	if u.id not in r.like_users:
		update_likes(r)
	return redirect(url_for("topic.detail", topic_id=r.topic_id))


def update_comments(topic):
	topic.comments += 1
	topic.update()


def update_likes(reply):
	reply.like_users.append(reply.user_id)
	reply.likes += 1
	reply.update()
