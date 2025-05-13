from flask import jsonify, session
from models import db
from models.setup import Setup
from models.user import User, RoleEnum
import logging
from . import setup_bp


@setup_bp.route("/status", methods=["GET"])
def get_setup_status():
    setup_record = Setup.query.first()
    if setup_record and setup_record.completed:
        logged_in = "logged_in" in session
        logging.info("Setup status retrieved successfully.")
        return jsonify(no_users=False, logged_in=logged_in)
    else:
        logging.info("Setup status retrieved successfully.")
        return jsonify(no_users=True)


@setup_bp.route("/finish", methods=["POST"])
def finish_setup():
    if not User.query.filter_by(role=RoleEnum.ADMIN).first():
        logging.error("Setup finish failed: No admin user created.")
        return jsonify(success=False, message="You must create at least one admin user before!")

    setup_record = Setup.query.first()
    if setup_record:
        setup_record.completed = True
    else:
        setup_record = Setup(completed=True)
        db.session.add(setup_record)
    db.session.commit()
    logging.info("Setup finished!")
    return jsonify(success=True)
