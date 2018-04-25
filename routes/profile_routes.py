from flask import (
	Blueprint,
	render_template,
	redirect,
	url_for,
	request,
)
from model.User import current_user
from model.User import User

profile_routes = Blueprint("profile", __name__)

@profile_routes.route("/<int:user_id>")
def profile(user_id):
	cur_user = current_user()
	view_user = User.find_by_id(user_id)
	return render_template("profile/profile.html", current_user=cur_user, view_user=view_user)


@profile_routes.route("/edit", methods=["GET", "POST"])
def edit():
	user = current_user()
	if not user:
		return redirect(url_for("auth.login"))
	if request.method == "GET":
		return render_template("profile/edit_profile.html", user=user)
	else:
		form = request.form
		for k, v in form.items():
			setattr(user, k, v)
		user.update()
		return redirect("/profile/{}".format(user.id))
