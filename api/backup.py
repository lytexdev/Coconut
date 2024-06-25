import os
import subprocess
import threading
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv

load_dotenv()

backup_bp = Blueprint("backup_api", __name__)


def run_backup(source_path, destination_path, max_backups, result):
    try:
        subprocess.run(
            [
                "./static/scripts/backup.sh",
                source_path,
                destination_path,
                str(max_backups),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        backup_files = sorted(os.listdir(destination_path))

        if len(backup_files) > max_backups:
            result["oldest_backup"] = backup_files[0]

    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
        result["error"] = str(e)


@backup_bp.route("/create_backup", methods=["POST"])
def create_backup():
    source_path = os.getenv("BACKUP_SOURCE_PATH")
    destination_path = os.getenv("BACKUP_DESTINATION_PATH")
    max_backups = int(os.getenv("BACKUP_DELETE_ALERT", "5"))

    result = {}
    thread = threading.Thread(
        target=run_backup, args=(source_path, destination_path, max_backups, result)
    )
    thread.start()
    thread.join()

    if "error" in result:
        return jsonify({"message": "Backup failed", "error": result["error"]}), 500

    oldest_backup = result.get("oldest_backup", None)
    return jsonify({"message": "Backup created", "oldest_backup": oldest_backup})


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
