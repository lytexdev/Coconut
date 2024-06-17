from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from flask import Flask
from flask_migrate import Migrate
from models import db
from views.auth import auth_bp
from views.main import main_bp
from api.system_info import system_info_bp
from api.backup import backup_bp
from api.docker_container import docker_bp

app = Flask(
    __name__, static_folder="static", static_url_path="", template_folder="templates"
)
app.config.from_object(Config)
rate_limiter = Limiter(get_remote_address, app=app, default_limits=[Config.RATE_LIMIT])

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(system_info_bp, url_prefix="/api")
app.register_blueprint(backup_bp, url_prefix="/api")
app.register_blueprint(docker_bp, url_prefix="/api")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
