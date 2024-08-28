from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_limiter.util import get_remote_address
from config import Config
import logging

from middleware import check_ip_blacklist, check_ip_whitelist, check_for_setup, content_security_policy, require_login, x_content_type_options, x_frame_options, configure_cors
from models import db
from urls import register_blueprints

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

# ----------------- URL and Blueprint Registration ----------------- #
register_blueprints(app)

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

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG == "True")
