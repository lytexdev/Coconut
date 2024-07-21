from flask import request, redirect, url_for, session
from models import Setup, User


def check_for_setup():
    """
    Middleware function to check if the setup has been completed.
    If not, it redirects to the setup page, allowing access only to setup-related endpoints.
    """
    setup_record = Setup.query.first()
    
    if not setup_record or not setup_record.completed:
        allowed_endpoints = [
            "setup.create_user",
            "setup.set_modules",
            "setup.get_setup_status",
            "setup.finish_setup",
            "setup.setup_index",
            "setup.get_available_modules"
        ]
        
        if request.endpoint not in allowed_endpoints:
            if request.endpoint and not request.endpoint.startswith("static"):
                return redirect(url_for("setup.setup_index"))
    else:
        if request.endpoint in ["setup.create_user", "setup.set_modules", "setup.get_setup_status", "setup.finish_setup", "setup.setup_index"]:
            return redirect(url_for("auth.login"))


def require_login():
    """
    Middleware function to ensure that users are logged in to access the application.
    If not logged in, it redirects to the login page.
    Certain endpoints are allowed without login (e.g., login, setup).
    """
    setup_record = Setup.query.first()
    
    if setup_record and setup_record.completed:
        allowed_endpoints = [
            "auth.login",
            "setup.create_user",
            "setup.set_modules",
            "setup.get_setup_status",
            "setup.finish_setup",
            "setup.setup_index",
            "setup.get_available_modules"
        ]
        if "logged_in" not in session and request.endpoint not in allowed_endpoints:
            if request.endpoint and not request.endpoint.startswith("static"):
                return redirect(url_for("auth.login"))
