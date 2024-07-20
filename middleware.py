from flask import request, redirect, url_for
from models import Setup, User


def check_for_setup():
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