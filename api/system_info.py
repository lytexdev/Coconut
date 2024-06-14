from flask import Blueprint, jsonify
import psutil

system_info_bp = Blueprint('api', __name__)

@system_info_bp.route('system_info')
def system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/')
    disk_used = disk_usage.used // (2**30)  # in GB
    disk_total = disk_usage.total // (2**30)  # in GB
    disk_usage_percent = disk_usage.percent

    return jsonify(
        cpu_usage=cpu_usage,
        ram_usage=ram_usage,
        disk_used=f"{disk_used}GB/{disk_total}GB ({disk_usage_percent}%)"
    )
