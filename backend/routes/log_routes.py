from flask import Blueprint, request, jsonify
from backend.models import db, DailyLog, Task
from datetime import datetime
from sqlalchemy.orm import joinedload

log_bp = Blueprint('log_bp', __name__, url_prefix='/api/logs')

@log_bp.route('/add', methods=['POST'])
def add_log():
    data = request.get_json() or {}
    user_id = data.get('user_id')

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "user_id must be a valid integer"}), 400

    if user_id <= 0:
        return jsonify({"error": "user_id is required"}), 400

    date_str = data.get('date')
    log_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
    tasks_data = data.get('tasks', [])

    if not isinstance(tasks_data, list):
        return jsonify({"error": "tasks must be a list"}), 400

    new_log = DailyLog(
        user_id=user_id,
        date=log_date,
        study_hours=data.get('study_hours', 0),
        screen_time_hours=data.get('screen_time_hours', 0),
        mood_score=data.get('mood_score', 5)
    )
    db.session.add(new_log)
    db.session.flush() # Get the new_log.id before committing

    # Add tasks if provided
    for task_name in tasks_data:
        cleaned_task = str(task_name).strip()
        if not cleaned_task:
            continue

        # DB column is VARCHAR(255), keep value safe for insert.
        new_task = Task(log_id=new_log.id, task_name=cleaned_task[:255], is_completed=False)
        db.session.add(new_task)

    db.session.commit()
    return jsonify({"message": "Log added successfully", "log": new_log.to_dict()}), 201

@log_bp.route('/fetch', methods=['GET'])
def fetch_logs():
    user_id = request.args.get('user_id', type=int)
    if not user_id or user_id <= 0:
        return jsonify({"error": "user_id is required"}), 400

    logs = (
        DailyLog.query.options(joinedload(DailyLog.tasks))
        .filter_by(user_id=user_id)
        .order_by(DailyLog.date.desc())
        .all()
    )
    return jsonify([log.to_dict() for log in logs]), 200

@log_bp.route('/update/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "user_id must be a valid integer"}), 400

    log = DailyLog.query.filter_by(id=log_id, user_id=user_id).first()
    if not log:
        return jsonify({"error": "Log not found for this user"}), 404

    if 'study_hours' in data: log.study_hours = data['study_hours']
    if 'screen_time_hours' in data: log.screen_time_hours = data['screen_time_hours']
    if 'mood_score' in data: log.mood_score = data['mood_score']

    db.session.commit()
    return jsonify({"message": "Log updated successfully", "log": log.to_dict()}), 200

@log_bp.route('/delete/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    user_id = request.args.get('user_id', type=int)
    if not user_id or user_id <= 0:
        return jsonify({"error": "user_id is required"}), 400

    log = DailyLog.query.filter_by(id=log_id, user_id=user_id).first()
    if not log:
        return jsonify({"error": "Log not found for this user"}), 404

    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Log deleted successfully"}), 200


@log_bp.route('/<int:log_id>/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(log_id, task_id):
    data = request.get_json() or {}
    if 'is_completed' not in data:
        return jsonify({"error": "is_completed is required"}), 400

    user_id = data.get('user_id')
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "user_id must be a valid integer"}), 400

    log = DailyLog.query.filter_by(id=log_id, user_id=user_id).first()
    if not log:
        return jsonify({"error": "Log not found for this user"}), 404

    task = Task.query.filter_by(id=task_id, log_id=log.id).first()
    if not task:
        return jsonify({"error": "Task not found for this log"}), 404

    task.is_completed = bool(data.get('is_completed'))
    db.session.commit()

    return jsonify({
        "message": "Task status updated successfully",
        "task": task.to_dict()
    }), 200
