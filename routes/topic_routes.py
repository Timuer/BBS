from flask import (
	Blueprint,
	render_template,
	request,
	session,
	redirect,
	url_for,
)
from model.Topic import Topic
from model.User import User
from model.Reply import Reply

topic_routes = Blueprint("topic", __name__)


@topic_routes.route("/")
def index():
	topics = Topic.all()
	user_id = session.get("user_id", "")
	user = User.find_by_id(user_id)
	return render_template("topic/index.html", user=user, topics=topics)


@topic_routes.route("/add", methods=["GET", "POST"])
def add():
	user_id = session.get("user_id", "")
	u = User.find_by_id(user_id)
	if not u:
		return redirect(url_for("auth.login"))
	if request.method == "GET":
		return render_template("topic/add.html", user_id=user_id)
	Topic.new(request.form)
	return redirect(url_for(".index"))


@topic_routes.route("/t/<topic_id>")
def detail(topic_id):
	t = Topic.find_by_id(topic_id)
	t.views += 1
	t.update()
	user_id = session.get("user_id", "")
	u = User.find_by_id(user_id)
	rs = Reply.find_by(topic_id=topic_id)
	rs.sort(key=lambda x: x.floor)
	floor_count = len(rs) + 1
	return render_template("topic/detail.html",
						   topic=t,
						   user=u,
						   replies=rs,
						   floor_count=floor_count)