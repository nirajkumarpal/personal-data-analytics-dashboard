from flask import Blueprint, request, jsonify
from backend.models import db, User

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/api/goals')

@goals_bp.route('/set', methods=['POST'])
def set_goal():
    """Set or update the user's daily study goal"""
    data = request.get_json()
    user_id = data.get('user_id')
    study_goal = data.get('study_goal')

    if not user_id or study_goal is None:
        return jsonify({"error": "user_id and study_goal are required"}), 400

    user = User.query.get_or_404(user_id)
    user.study_goal = float(study_goal)
    db.session.commit()

    return jsonify({
        "message": "Goal updated successfully",
        "study_goal": user.study_goal
    }), 200


@goals_bp.route('/get', methods=['GET'])
def get_goal():
    """Get the user's current daily study goal and today's progress"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get_or_404(user_id)
    
    # Get today's total study hours
    from datetime import date
    from models import DailyLog
    today_logs = DailyLog.query.filter_by(user_id=user_id, date=date.today()).all()
    today_study = sum(l.study_hours for l in today_logs)

    # Calculate progress percentage
    goal = user.study_goal if user.study_goal > 0 else 6.0
    progress = min(round((today_study / goal) * 100, 1), 100)

    return jsonify({
        "study_goal": goal,
        "today_study_hours": today_study,
        "progress_percent": progress
    }), 200
