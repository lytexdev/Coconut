from flask import Blueprint, render_template, redirect, url_for, session, jsonify
import os
import psutil
from config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return render_template('app.html')


@main_bp.route('/system_info')
def system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    disk_stats = psutil.disk_io_counters()
    return jsonify(cpu_usage=cpu_usage, ram_usage=ram_usage, disk_usage=disk_usage)


@main_bp.route('/shutdown', methods=['POST'])
def shutdown():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    os.system(Config.SHUTDOWN_COMMAND)
    return redirect(url_for('main.index'))


@main_bp.route('/reboot', methods=['POST'])
def reboot():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    os.system(Config.REBOOT_COMMAND)
    return redirect(url_for('main.index'))
