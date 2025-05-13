from flask import Blueprint, jsonify
import psutil
import time

system_info_bp = Blueprint("api", __name__)


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g.:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@system_info_bp.route("system_info")
def system_info():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory usage
    virtual_memory = psutil.virtual_memory()
    ram_total = get_size(virtual_memory.total)
    ram_available = get_size(virtual_memory.available)
    ram_used = get_size(virtual_memory.used)
    ram_percent = virtual_memory.percent

    # Swap memory usage
    swap_memory = psutil.swap_memory()
    swap_total = get_size(swap_memory.total)
    swap_used = get_size(swap_memory.used)
    swap_free = get_size(swap_memory.free)
    swap_percent = swap_memory.percent

    # Disk usage
    disk_usage = psutil.disk_usage("/")
    disk_used = get_size(disk_usage.used)
    disk_total = get_size(disk_usage.total)
    disk_percent = disk_usage.percent

    # Disk I/O
    disk_io = psutil.disk_io_counters()
    disk_read = get_size(disk_io.read_bytes)
    disk_write = get_size(disk_io.write_bytes)
    
    # System uptime
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    days = int(uptime // (24 * 3600))
    hours = int((uptime % (24 * 3600)) // 3600)
    minutes = int((uptime % 3600) // 60)
    uptime_str = f"{days} days, {hours} hours, {minutes} minutes"

    return jsonify(
        cpu_usage=cpu_usage,
        ram_total=ram_total,
        ram_available=ram_available,
        ram_used=ram_used,
        ram_percent=ram_percent,
        swap_total=swap_total,
        swap_used=swap_used,
        swap_free=swap_free,
        swap_percent=swap_percent,
        disk_total=disk_total,
        disk_used=disk_used,
        disk_percent=disk_percent,
        disk_read=disk_read,
        disk_write=disk_write,
        uptime=uptime_str,
    )
