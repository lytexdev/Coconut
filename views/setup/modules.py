import os
import json
import logging
from flask import jsonify, request
from models import db
from models.module import Module, ModuleEnum
import docker
from . import setup_bp


def load_json_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f).get("modules", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load JSON data from {file_path}: {str(e)}")
        return []


def check_docker():
    try:
        client = docker.from_env()
        client.ping()
        logging.info("Docker is available.")
        return True
    except docker.errors.DockerException as e:
        logging.warning(f"Docker is not available: {str(e)}")
        return False


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
    modules_list = [{"name": module.name.name, "order": module.order} for module in enabled_modules]
    logging.info("Modules configuration retrieved successfully.")
    return jsonify(modules=modules_list)


@setup_bp.route("/available-modules", methods=["GET"])
def get_available_modules():
    core_modules_path = 'coconut-shell/src/core_modules.json'
    custom_modules_path = 'coconut-shell/src/custom_modules.json'

    logging.info(f"Loading core modules from: {core_modules_path}")
    core_modules = load_json_data(core_modules_path)

    logging.info(f"Loading custom modules from: {custom_modules_path}")
    custom_modules = load_json_data(custom_modules_path)

    # Merge core and custom modules
    all_modules = core_modules + custom_modules
    logging.info(f"All merged modules: {all_modules}")

    docker_available = check_docker()

    available_modules = [
        module for module in all_modules
        if module["enum"] != "DOCKER" or docker_available
    ]

    logging.info(f"Available modules: {available_modules}")
    return jsonify(modules=available_modules)
