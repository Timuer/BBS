from flask import (
	Blueprint,
	render_template,
	request,
	redirect,
	url_for,
)
from model.User import current_user
from model.Board import Board

board_routes = Blueprint("board", __name__)

@board_routes.route("/add", methods=["GET", "POST"])
def add():
	u = current_user()
	if not u:
		return redirect(url_for("topic.index"))
	if request.method == "GET":
		return render_template("board/add_board.html")
	else:
		Board.new(request.form)
	return redirect(url_for("topic.index"))