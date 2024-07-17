from flask import Blueprint, jsonify, request
import docker
import logging

docker_bp = Blueprint("docker_api", __name__)
client = docker.from_env()


@docker_bp.route("/docker_containers")
def docker_containers():
    containers = client.containers.list(all=True)
    container_info = [
        {
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
        }
        for c in containers
    ]
    return jsonify(container_info)


@docker_bp.route("/docker_start", methods=["POST"])
def docker_start():
    data = request.get_json()
    container_id = data.get("id")
    container = client.containers.get(container_id)
    container.start()
    logging.info(f"Container {container_id} started.")
    return jsonify({"status": "started"})


@docker_bp.route("/docker_stop", methods=["POST"])
def docker_stop():
    data = request.get_json()
    container_id = data.get("id")
    container = client.containers.get(container_id)
    container.stop()
    logging.info(f"Container {container_id} stopped.")
    return jsonify({"status": "stopped"})


@docker_bp.route("/docker_remove", methods=["POST"])
def docker_remove():
    data = request.get_json()
    container_id = data.get("id")
    container = client.containers.get(container_id)
    container.remove()
    logging.info(f"Container {container_id} removed.")
    return jsonify({"status": "removed"})
