from flask import Blueprint, render_template, redirect, url_for, session, jsonify
import os
import psutil
from config import Config

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("auth.login"))
    return render_template("index.html")


@main_bp.route('/api/shutdown', methods=['POST'])
def shutdown():
    if not session.get('logged_in'):
        return jsonify(success=False, message="Unauthorized"), 401
    os.system(Config.SHUTDOWN_COMMAND)
    return jsonify(success=True, message="Shutdown initiated")


@main_bp.route('/api/reboot', methods=['POST'])
def reboot():
    if not session.get('logged_in'):
        return jsonify(success=False, message="Unauthorized"), 401
    os.system(Config.REBOOT_COMMAND)
    return jsonify(success=True, message="Reboot initiated")
