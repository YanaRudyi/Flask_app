from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, request, jsonify

from tables import Task, db

task_blueprint = Blueprint('task', __name__, url_prefix='/tasks')


@task_blueprint.route('', methods=['POST'])
def create_task():
    """Create a new task."""
    task_data = request.json
    new_task = Task(title=task_data['title'], status=task_data['status'])
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "status": new_task.status,
        "created_on": new_task.created_on,
        "updated_on": new_task.updated_on
    }), HTTPStatus.CREATED


@task_blueprint.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    """Update an existing task by its ID."""
    task = Task.query.get(task_id)
    if task:
        task_data = request.json
        task.title = task_data['title']
        task.status = task_data['status']
        task.updated_on = datetime.utcnow()
        db.session.commit()
        return jsonify({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "created_on": task.created_on,
            "updated_on": task.updated_on
        }), HTTPStatus.OK
    else:
        return jsonify({'message': 'Task not found'}), HTTPStatus.NOT_FOUND


@task_blueprint.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """Delete a task by its ID."""
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    else:
        return jsonify({'message': 'Task not found'}), HTTPStatus.NOT_FOUND


@task_blueprint.route('', methods=['GET'])
def get_tasks():
    """Get a list of tasks."""
    status = request.args.get('status')
    if status is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(status=status)
    task_list = [{
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "created_on": task.created_on,
        "updated_on": task.updated_on
    } for task in tasks]
    return jsonify({"tasks": task_list})


@task_blueprint.route('/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id: int):
    """Get a task by its ID."""
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "created_on": task.created_on,
            "updated_on": task.updated_on
        }), HTTPStatus.OK
    else:
        return jsonify({'message': 'Task not found'}), HTTPStatus.NOT_FOUND
