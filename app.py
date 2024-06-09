from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from views.auth import auth_bp
from views.main import main_bp
from api.system_info import api_bp
from api.docker_container import docker_bp

app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app.config.from_object(Config)

rate_limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[Config.RATE_LIMIT]
)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(docker_bp, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
