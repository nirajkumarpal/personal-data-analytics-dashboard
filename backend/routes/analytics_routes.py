from flask import Blueprint, request, jsonify
from models import DailyLog
from sqlalchemy.orm import joinedload
from analytics.insights import (
    calculate_productivity_score,
    generate_smart_insights,
    generate_weekly_summary
)

analytics_bp = Blueprint('analytics_bp', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/summary', methods=['GET'])
def get_summary():
    """Main dashboard data: chart data + insights + productivity score + weekly summary"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Fetch last 30 logs for trends
    logs = (
        DailyLog.query.options(joinedload(DailyLog.tasks))
        .filter_by(user_id=user_id)
        .order_by(DailyLog.date.desc())
        .limit(30)
        .all()
    )

    # 1. Chart Data (ascending order for display)
    chart_data = []
    for log in reversed(logs):
        chart_data.append({
            "date": log.date.strftime('%b %d'),
            "study_hours": log.study_hours,
            "screen_time": log.screen_time_hours,
            "mood": log.mood_score
        })

    # 2. Smart Insights
    text_insights = generate_smart_insights(logs)

    # 3. Productivity Score (average of recent logs)
    productivity_scores = [
        calculate_productivity_score(log.study_hours, log.screen_time_hours, log.mood_score)
        for log in logs
    ]
    productivity_score = round(sum(productivity_scores) / len(productivity_scores), 1) if productivity_scores else 0

    # 4. Stats
    total_study = sum(l.study_hours for l in logs)
    total_screen = sum(l.screen_time_hours for l in logs)
    avg_mood = round(sum(l.mood_score for l in logs) / len(logs), 1) if logs else 0
    productive_days = len([l for l in logs if l.study_hours >= 4])
    total_tasks = sum(len(l.tasks) for l in logs)
    completed_tasks = sum(1 for l in logs for t in l.tasks if t.is_completed)
    task_completion_percent = round((completed_tasks / total_tasks) * 100, 1) if total_tasks else 0

    # 5. Weekly Summary
    weekly = generate_weekly_summary(logs[:7])  # Last 7 logs

    return jsonify({
        "chart_data": chart_data,
        "insights": {
            "total_study_hours": round(total_study, 2),
            "total_screen_time": round(total_screen, 2),
            "average_mood": avg_mood,
            "productive_days_count": productive_days,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "task_completion_percent": task_completion_percent,
            "text_insights": text_insights,
            "productivity_score": productivity_score
        },
        "weekly_summary": weekly
    }), 200


@analytics_bp.route('/weekly-summary', methods=['GET'])
def weekly_summary():
    """Dedicated endpoint for weekly summary with SQL-like aggregation"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    logs = DailyLog.query.filter_by(user_id=user_id).order_by(DailyLog.date.desc()).limit(7).all()
    summary = generate_weekly_summary(logs)
    return jsonify(summary), 200


@analytics_bp.route('/insights', methods=['GET'])
def get_insights():
    """Dedicated endpoint for smart insights"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    logs = DailyLog.query.filter_by(user_id=user_id).order_by(DailyLog.date.desc()).limit(30).all()
    insights = generate_smart_insights(logs)

    # Per-log productivity scores
    scores = []
    for log in reversed(logs):
        scores.append({
            "date": log.date.strftime('%b %d'),
            "score": calculate_productivity_score(log.study_hours, log.screen_time_hours, log.mood_score)
        })

    return jsonify({
        "insights": insights,
        "productivity_scores": scores
    }), 200
