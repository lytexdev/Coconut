from flask import request, redirect, url_for, session, jsonify
from flask_cors import CORS
from models import Setup, User
from config import Config
import urls


def check_for_setup():
    setup_record = Setup.query.first()
    
    if not setup_record or not setup_record.completed:
        if request.endpoint not in urls.allowed_endpoints:
            if request.endpoint and not request.endpoint.startswith("static"):
                return redirect(url_for("setup.setup_index"))


def require_login():
    setup_record = Setup.query.first()
    
    if setup_record and setup_record.completed:
        if "logged_in" not in session and request.endpoint not in urls.require_login_endpoints:
            if request.endpoint and not request.endpoint.startswith("static"):
                return redirect(url_for("auth.login"))


def configure_cors(app):
    """
    Configure CORS settings.
    """
    allowed_origins = Config.ALLOWED_ORIGINS
    if allowed_origins == "*":
        CORS(app, resources={r"/*": {"origins": "*"}})
    else:
        allowed_origins_list = allowed_origins.split(",")
        CORS(app, resources={r"/*": {"origins": allowed_origins_list}})


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


def content_security_policy(response):
    """
    Middleware function to add Content Security Policy headers to each response.
    Adjusted to allow resources from the same origin.
    """
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-src 'self'; "
        "media-src 'self'; "
        "object-src 'none'; "
        "child-src 'self'; "
        "frame-ancestors 'self'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )
    return response


def x_content_type_options(response):
    """
    Middleware function to add X-Content-Type-Options headers to each response.
    Prevents the browser from interpreting files as a different MIME type than what is specified.
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


def x_frame_options(response):
    """
    Middleware function to add X-Frame-Options headers to each response.
    Prevents the application from being embedded in a frame, protecting against clickjacking attacks.
    """
    response.headers["X-Frame-Options"] = "DENY"
    return response
