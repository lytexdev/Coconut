import os
import subprocess
import threading
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv

load_dotenv()

backup_bp = Blueprint("backup_api", __name__)

def run_backup(source_path, destination_path, max_backups):
    subprocess.run(
        ["./static/scripts/backup.sh", source_path, destination_path, max_backups],
        check=True,
        capture_output=True,
        text=True,
    )

    backup_files = sorted(os.listdir(destination_path))

    if len(backup_files) > int(max_backups):
        return backup_files[0]

    return None

@backup_bp.route("/create_backup", methods=["POST"])
def create_backup():
    source_path = os.getenv("BACKUP_SOURCE_PATH")
    destination_path = os.getenv("BACKUP_DESTINATION_PATH")
    max_backups = os.getenv("BACKUP_DELETE_ALERT", "5")

    def backup_thread():
        run_backup(source_path, destination_path, max_backups)
    
    thread = threading.Thread(target=backup_thread)
    thread.start()

    return jsonify({"message": "Backup started", "oldest_backup": None})


@backup_bp.route("/backup_count", methods=["GET"])
def backup_count():
    destination_path = os.getenv("BACKUP_DESTINATION_PATH")
    count = len(
        [
            name
            for name in os.listdir(destination_path)
            if os.path.isfile(os.path.join(destination_path, name))
        ]
    )
    return jsonify({"count": count})


@backup_bp.route("/list_backups", methods=["GET"])
def list_backups():
    destination_path = os.getenv("BACKUP_DESTINATION_PATH")
    backups = sorted(
        [
            name
            for name in os.listdir(destination_path)
            if os.path.isfile(os.path.join(destination_path, name))
        ]
    )
    return jsonify({"backups": backups})


@backup_bp.route("/delete_backup", methods=["POST"])
def delete_backup():
    destination_path = os.getenv("BACKUP_DESTINATION_PATH")
    data = request.get_json()
    backup_to_delete = data.get("backup_to_delete")

    try:
        os.remove(os.path.join(destination_path, backup_to_delete))
        return jsonify({"message": f"{backup_to_delete} deleted successfully"})
    except Exception as e:
        return (
            jsonify({"message": f"Error deleting {backup_to_delete}", "error": str(e)}),
            500,
        )
