from flask import Blueprint, jsonify, render_template, request, session
from models import db
from models.user import User, RoleEnum
import bcrypt

setup_bp = Blueprint("setup", __name__)


@setup_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    if not username or not password or not role:
        return jsonify(success=False, message="All fields are required.")
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(success=False, message="Username already exists.")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User(username=username, password_hash=password_hash, role=RoleEnum[role])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(success=True)


@setup_bp.route("/status", methods=["GET"])
def get_setup_status():
    if User.query.first():
        logged_in = "logged_in" in session
        return jsonify(no_users=False, logged_in=logged_in)
    else:
        return jsonify(no_users=True)


@setup_bp.route("/", methods=["GET"])
def setup_index():
    return render_template("index.html")
