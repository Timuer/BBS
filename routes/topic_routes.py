from flask import (
	Blueprint,
	render_template,
	request,
	redirect,
	url_for,
)
from model.Topic import Topic
from model.User import current_user
from model.Reply import Reply
from model.Board import Board

topic_routes = Blueprint("topic", __name__)


@topic_routes.route("/")
def index():
	board_id = request.args.get("board", "")
	topics = get_topics(board_id)
	boards = Board.all()
	user = current_user()
	return render_template("topic/index.html",
						   user=user,
						   topics=topics,
						   board_id=board_id,
						   boards=boards)


@topic_routes.route("/add", methods=["GET", "POST"])
def add():
	u = current_user()
	if not u:
		return redirect(url_for("auth.login"))
	if request.method == "GET":
		boards = Board.all()
		return render_template("topic/add.html", user_id=u.id, boards=boards)
	Topic.new(request.form)
	return redirect(url_for(".index"))


@topic_routes.route("/t/<topic_id>")
def detail(topic_id):
	t = Topic.find_by_id(topic_id)
	u = current_user()
	rs = Reply.find_by(topic_id=topic_id)
	update_views(t)
	rs.sort(key=lambda x: x.floor)
	floor_count = len(rs) + 1
	return render_template("topic/detail.html",
						   topic=t,
						   user=u,
						   replies=rs,
						   floor_count=floor_count)


def update_views(topic):
	topic.views += 1
	topic.update()


def get_topics(board_id):
	if not board_id:
		return Topic.all()
	else:
		return [t for t in Topic.all() if t.board_id == board_id]
