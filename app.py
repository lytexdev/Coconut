from flask import Flask, redirect, request, url_for, render_template
from flask_limiter import Limiter
from flask_cors import CORS
from flask_limiter.util import get_remote_address
from config import Config
import logging
from flask_migrate import Migrate

from middleware import check_ip_blacklist, check_ip_whitelist, check_for_setup, require_login
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
                    handlers=[logging.FileHandler("logs/coconut.log"), logging.StreamHandler()])


# ----------------- CORS ----------------- #
allowed_origins = Config.ALLOWED_ORIGINS
if allowed_origins == "*":
    CORS(app, resources={r"/*": {"origins": "*"}})
else:
    allowed_origins_list = allowed_origins.split(",")
    CORS(app, resources={r"/*": {"origins": allowed_origins_list}})


# ----------------- Database ----------------- #
db.init_app(app)
migrate = Migrate(app, db)


# ----------------- Blueprints ----------------- #
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(setup_bp, url_prefix="/setup")
app.register_blueprint(system_info_bp, url_prefix="/api")
app.register_blueprint(backup_bp, url_prefix="/api")


# ----------------- Docker Integration ----------------- #
try:
    import docker
    client = docker.from_env()
    from api.docker_container import docker_bp
    app.register_blueprint(docker_bp, url_prefix="/api")
except (ImportError, docker.errors.DockerException) as e:
    logging.warning("Docker is not available. Skipping Docker Integration.")


# ----------------- Middleware ----------------- #
app.before_request(check_ip_blacklist)
app.before_request(check_ip_whitelist)
app.before_request(check_for_setup)
app.before_request(require_login)

# ----------------- Index Route ----------------- #
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG == "True")