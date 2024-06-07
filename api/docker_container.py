from flask import Blueprint, jsonify, request
import docker

docker_bp = Blueprint('docker_api', __name__)
client = docker.from_env()

@docker_bp.route('/docker_containers')
def docker_containers():
    containers = client.containers.list(all=True)
    container_info = [{'id': c.id, 'name': c.name, 'status': c.status, 'image': c.image.tags[0] if c.image.tags else 'unknown'} for c in containers]
    return jsonify(container_info)


@docker_bp.route('/docker_start', methods=['POST'])
def docker_start():
    container_id = request.json.get('id')
    container = client.containers.get(container_id)
    container.start()
    return jsonify({'status': 'started'})


@docker_bp.route('/docker_stop', methods=['POST'])
def docker_stop():
    container_id = request.json.get('id')
    container = client.containers.get(container_id)
    container.stop()
    return jsonify({'status': 'stopped'})


@docker_bp.route('/docker_remove', methods=['POST'])
def docker_remove():
    container_id = request.json.get('id')
    container = client.containers.get(container_id)
    container.remove()
    return jsonify({'status': 'removed'})
