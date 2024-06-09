from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from config import Config
import bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if username == Config.USERNAME and bcrypt.checkpw(
            password.encode("utf-8"), Config.HASHED_PASSWORD.encode("utf-8")
        ):
            session["logged_in"] = True
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Invalid credentials. Please try again.")
    return render_template("index.html")


@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("auth.login"))
