from flask import Flask, redirect, request, url_for, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
import logging
from flask_migrate import Migrate

from models import db, User, Setup
from views.auth import auth_bp
from views.main import main_bp
from views.setup import setup_bp
from api.system_info import system_info_bp
from api.backup import backup_bp


# ----------------- Flask App ----------------- #
app = Flask(__name__, static_folder="static", static_url_path="", template_folder="templates")
app.config.from_object(Config)
rate_limiter = Limiter(get_remote_address, app=app, default_limits=[Config.RATE_LIMIT])
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler("coconut.log"), logging.StreamHandler()])


# ----------------- Database ----------------- #
db.init_app(app)
migrate = Migrate(app, db)


# ----------------- Blueprints ----------------- #
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(setup_bp, url_prefix="/setup")
app.register_blueprint(system_info_bp, url_prefix="/api")
app.register_blueprint(backup_bp, url_prefix="/api")


# ----------------- Check Docker Integration ----------------- #
try:
    import docker
    client = docker.from_env()
    from api.docker_container import docker_bp
    app.register_blueprint(docker_bp, url_prefix="/api")
except (ImportError, docker.errors.DockerException) as e:
    logging.warning("Docker is not available. Skipping Docker Integration.")


# ----------------- Setup Check ----------------- #
@app.before_request
def check_for_setup():
    setup_record = Setup.query.first()
    if not User.query.first() or (setup_record and not setup_record.completed):
        if request.endpoint not in ["setup.create_user", "setup.set_modules", "setup.get_setup_status", "setup.finish_setup", "setup.setup_index"]:
            if request.endpoint and not request.endpoint.startswith("static"):
                return redirect(url_for("setup.setup_index"))


# ----------------- Index Route ----------------- #
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
