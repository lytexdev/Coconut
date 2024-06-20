from flask import Blueprint, jsonify, session
import os
import psutil
from config import Config

system_info_bp = Blueprint("api", __name__)


@system_info_bp.route("system_info")
def system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/")
    disk_used = disk_usage.used // (2**30)  # in GB
    disk_total = disk_usage.total // (2**30)  # in GB
    disk_usage_percent = disk_usage.percent

    return jsonify(
        cpu_usage=cpu_usage,
        ram_usage=ram_usage,
        disk_used=f"{disk_used}GB/{disk_total}GB ({disk_usage_percent}%)",
    )


@system_info_bp.route("/api/shutdown", methods=["POST"])
def shutdown():
    if not session.get("logged_in"):
        return jsonify(success=False, message="Unauthorized"), 401
    os.system(Config.SHUTDOWN_COMMAND)
    return jsonify(success=True, message="Shutdown initiated")


@system_info_bp.route("/api/reboot", methods=["POST"])
def reboot():
    if not session.get("logged_in"):
        return jsonify(success=False, message="Unauthorized"), 401
    os.system(Config.REBOOT_COMMAND)
    return jsonify(success=True, message="Reboot initiated")
