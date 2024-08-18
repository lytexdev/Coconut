from flask import jsonify, request
from models import db
from models.user import User, RoleEnum
import logging
from . import setup_bp


@setup_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        logging.error("User creation failed: Missing fields.")
        return jsonify(success=False, message="All fields are required.")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        logging.error(f"User creation failed: Username {username} already exists.")
        return jsonify(success=False, message="Username already exists.")

    new_user = User(username=username, role=RoleEnum[role])
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()
    logging.info(f"User {username} created successfully.")
    return jsonify(success=True)
