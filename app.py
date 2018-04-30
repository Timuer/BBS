from flask import Flask
from flask import redirect
from flask import url_for
from routes.topic_routes import topic_routes
from routes.auth_routes import auth_routes
from routes.reply_routes import reply_routes
from routes.board_routes import board_routes
from routes.profile_routes import profile_routes
from config import secret_key

app = Flask(__name__)
app.secret_key = secret_key

app.register_blueprint(topic_routes, url_prefix="/topic")
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(reply_routes, url_prefix="/reply")
app.register_blueprint(board_routes, url_prefix="/board")
app.register_blueprint(profile_routes, url_prefix="/profile")


@app.route("/", methods=["GET"])
def index():
	return redirect(url_for("topic.index"))


if __name__ == "__main__":
	app.run(debug=True)
