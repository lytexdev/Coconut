from flask import Flask, redirect, request, url_for, render_template, jsonify
from flask_limiter import Limiter
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_limiter.util import get_remote_address
from config import Config
import importlib
import logging
import os

from middleware import check_ip_blacklist, check_ip_whitelist, check_for_setup, content_security_policy, require_login, x_content_type_options, x_frame_options, configure_cors
from models import db, User, Setup
from views.auth import auth_bp
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
csrf = CSRFProtect(app)


# ----------------- CORS ----------------- #
configure_cors(app)

# ----------------- Database ----------------- #
db.init_app(app)
migrate = Migrate(app, db)


# ----------------- URL Prefixes ----------------- #
app.register_blueprint(auth_bp)
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

app.after_request(content_security_policy)
app.after_request(x_content_type_options)
app.after_request(x_frame_options)


# ----------------- CSRF Route ----------------- #
@app.route("/api/csrf-token", methods=["GET"])
def csrf_token():
    """
    Generate a CSRF Token for the client
    """
    token = generate_csrf()
    return jsonify(csrf_token=token)


# ----------------- Index Route ----------------- #
@app.route("/")
def index():  
    return render_template("index.html")


# ----------------- Custom Module Registration ----------------- #
def register_custom_modules(app):
    custom_modules_dir = os.path.join(os.path.dirname(__file__), 'custom_modules')

    if not os.path.exists(custom_modules_dir):
        logging.info(f"No custom modules directory found at {custom_modules_dir}")
        return

    for module_name in os.listdir(custom_modules_dir):
        module_path = os.path.join(custom_modules_dir, module_name)
        if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, '__init__.py')):
            try:
                module = importlib.import_module(f'custom_modules.{module_name}')
                expected_bp_name = f'{module_name}_bp'
                
                if hasattr(module, expected_bp_name):
                    blueprint = getattr(module, expected_bp_name)
                    app.register_blueprint(blueprint, url_prefix="/api")
                    logging.info(f"Registered custom module: {module_name}")
                else:
                    logging.warning(f"No blueprint found in custom module {module_name}")

            except ImportError as e:
                logging.error(f"Failed to import custom module {module_name}: {e}")

register_custom_modules(app)


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG == "True")