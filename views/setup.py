from flask import Blueprint, jsonify, request, session, render_template
from models import db
from models.user import User, RoleEnum
from models.setup import Setup
from models.module import Module, ModuleEnum
import logging
import docker
import os
import json

setup_bp = Blueprint("setup", __name__)


def check_docker():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


@setup_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        logging.error("User creation failed: Missing fields.")
        return jsonify(success=False, message="All fields are required.")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        logging.error(f"User creation failed: Username {username} already exists.")
        return jsonify(success=False, message="Username already exists.")

    new_user = User(username=username, role=RoleEnum[role])
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()
    logging.info(f"User {username} created successfully.")
    return jsonify(success=True)


@setup_bp.route("/modules", methods=["POST"])
def set_modules():
    data = request.get_json()
    selected_modules = data.get("modules", [])

    for module_data in selected_modules:
        module_name = module_data.get("name").upper().replace(" ", "_")
        order = module_data.get("order")
        existing_module = Module.query.filter_by(name=ModuleEnum[module_name]).first()
        if existing_module:
            existing_module.order = order
            existing_module.enabled = True
        else:
            new_module = Module(name=ModuleEnum[module_name], enabled=True, order=order)
            db.session.add(new_module)

    db.session.commit()
    logging.info("Modules configuration saved successfully.")
    return jsonify(success=True)


@setup_bp.route("/modules", methods=["GET"])
def get_modules():
    enabled_modules = Module.query.filter_by(enabled=True).order_by(Module.order).all()
    modules_list = [
        {"name": module.name.name, "order": module.order} for module in enabled_modules
    ]
    logging.info("Modules configuration retrieved successfully.")
    return jsonify(modules=modules_list)


@setup_bp.route("/available-modules", methods=["GET"])
def get_available_modules():
    try:
        json_path = os.path.join(os.getcwd(), 'coconut-shell', 'src', 'core_modules.json')
        custom_json_path = os.path.join(os.getcwd(), 'coconut-shell', 'src', 'custom_modules.json')
        logging.info(f"Loading core modules from: {json_path}")
        
        if not os.path.exists(json_path):
            logging.error(f"modules.json file not found at: {json_path}")
            return jsonify(modules=[]), 404

        with open(json_path) as f:
            modules_data = json.load(f)
            logging.info(f"Loaded core modules: {modules_data}")

        custom_modules_data = []
        if os.path.exists(custom_json_path):
            with open(custom_json_path) as custom_f:
                custom_modules_data = json.load(custom_f).get("modules", [])
                logging.info(f"Loaded custom modules: {custom_modules_data}")
        
        # Merge core and custom modules
        all_modules = modules_data["modules"] + custom_modules_data

        docker_client = docker.from_env()
        docker_client.ping()
        docker_available = True
    except Exception as e:
        docker_available = False

    available_modules = [
        module for module in all_modules
        if module["enum"] != "DOCKER" or docker_available
    ]

    logging.info("Available modules retrieved successfully.")
    return jsonify(modules=available_modules)


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


@setup_bp.route("/", methods=["GET"])
def setup_index():
    return render_template("index.html")
