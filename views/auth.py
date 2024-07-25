from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from models import db
from models.user import User
import logging

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password_hash(password):
            session["logged_in"] = True
            session["user_id"] = str(user.id)
            session["role"] = user.role.value
            logging.info(f"User {username} logged in successfully.")
            return jsonify(success=True)
        else:
            logging.error(f"Login failed: Invalid credentials for user {username}.")
            return jsonify(success=False, message="Invalid credentials. Please try again.")
    return render_template("index.html")


@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("user_id", None)
    session.pop("role", None)
    logging.info("User logged out.")
    return redirect(url_for("auth.login"))
