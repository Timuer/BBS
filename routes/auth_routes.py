from model.User import User
from flask import (
	Blueprint,
	request,
	redirect,
	url_for,
	render_template,
	session,
)
from utils import generate_token

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return login_get()
	else:
		return login_post()


def login_get():
	token = generate_token()
	return render_template("login.html", token=token, messages="")


def login_post():
	form = request.form
	u = User.validate_login(form)
	if u:
		session["user_id"] = u.id
		session.permanent = True
		return redirect(url_for("topic.index"))
	else:
		token = generate_token()
		return render_template("login.html", token=token, messages="用户名或密码错误")


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return register_get()


def register_get():
	token = generate_token()
	return render_template("register.html", token=token, messages="")


def register_post():
	form = request.form
	is_success, messages = User.register(form)
	if is_success:
		return redirect(url_for(".login"))
	else:
		token = generate_token()
		return render_template("register.html", token=token, messages=messages)
