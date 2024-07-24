from flask import request, redirect, url_for, session, jsonify
from models import Setup, User
from config import Config


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


def check_ip_blacklist():
    """
    Middleware function to check if the request's IP address is in the blacklist.
    If the IP is in the blacklist, access is denied.
    """
    ip_blacklist = Config.IP_BLACKLIST.split(",")

    client_ip = request.remote_addr
    
    if client_ip in ip_blacklist:
        return jsonify({"message": "Access denied"}), 403
    

def check_ip_whitelist():
    """
    Middleware function to check if the request's IP address is in the whitelist.
    If WHITELIST is enabled and the IP is not in the whitelist, access is denied.
    """
    whitelist_enabled = Config.WHITELIST == "True"
    ip_whitelist = Config.IP_WHITELIST.split(", ")

    if whitelist_enabled:
        client_ip = request.remote_addr

        if client_ip not in ip_whitelist:
            return jsonify({"message": "Access denied"}), 403
