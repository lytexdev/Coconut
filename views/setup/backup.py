from flask import jsonify, request
from models import db
from models.backup import Backup
import logging
from . import setup_bp
import os


@setup_bp.route("/create-backup", methods=["POST"])
def create_backup():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    backup_path = data.get("backupPath")
    destination_path = data.get("destinationPath")
    excluded_paths = data.get("excludedPaths")
    scheduled_time = data.get("scheduledTime")
    max_backups = data.get("maxBackups")
    enabled = data.get("enabled")
    
    if not name or not backup_path or not destination_path:
        logging.error("Backup creation failed: Missing fields.")
        return jsonify(success=False, message="All fields are required.")
    
    if not os.path.exists(backup_path):
        logging.error(f"Backup creation failed: Backup path {backup_path} does not exist.")
        return jsonify(success=False, message="Backup path does not exist.")
    
    if not os.path.exists(destination_path):
        logging.error(f"Backup creation failed: Destination path {destination_path} does not exist.")
        return jsonify(success=False, message="Destination path does not exist.")
    
    backup = Backup(
        name=name,
        description=description,
        backup_path=backup_path,
        destination_path=destination_path,
        excluded_paths=excluded_paths,
        scheduled_time=scheduled_time,
        max_backups=max_backups,
        enabled=enabled
    )
    
    db.session.add(backup)
    db.session.commit()
    logging.info("Backup created successfully.")
    return jsonify(success=True)


@setup_bp.route("/backups", methods=["GET"])
def get_backups():
    backups = Backup.query.all()
    backups_list = [
        {
            "id": backup.id,
            "name": backup.name,
            "description": backup.description,
            "backupPath": backup.backup_path,
            "destinationPath": backup.destination_path,
            "excludedPaths": backup.excluded_paths,
            "scheduledTime": backup.scheduled_time,
            "maxBackups": backup.max_backups,
            "enabled": backup.enabled
        }
        for backup in backups
    ]
    logging.info("Backups retrieved successfully.")
    return jsonify(backups=backups_list)


@setup_bp.route("/backups/<int:backup_id>", methods=["DELETE"])
def delete_backup(backup_id):
    backup = Backup.query.get_or_404(backup_id)
    db.session.delete(backup)
    db.session.commit()
    logging.info(f"Backup {backup.name} deleted successfully.")
    return jsonify(success=True, message=f"Backup {backup.name} deleted successfully.")
