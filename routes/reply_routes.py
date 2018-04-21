from flask import (
	Blueprint,
	request,
	session,
	redirect,
	url_for,
)
from model.Reply import Reply
from model.Topic import Topic


reply_routes = Blueprint("reply", __name__)


@reply_routes.route("/add/<topic_id>", methods=["POST"])
def add(topic_id):
	user_id = session.get("user_id", None)
	if not user_id:
		return redirect(url_for("auth.login"))
	Reply.new(request.form)
	t = Topic.find_by_id(topic_id)
	t.comments += 1
	t.update()
	return redirect(url_for("topic.detail", topic_id=topic_id))

@reply_routes.route("/votes/<reply_id>")
def votes(reply_id):
	user_id = session.get("user_id", None)
	r = Reply.find_by_id(reply_id)
	if user_id not in r.like_users:
		r.like_users.append(user_id)
		r.likes += 1
		r.update()
	return redirect(url_for("topic.detail", topic_id=r.topic_id))
