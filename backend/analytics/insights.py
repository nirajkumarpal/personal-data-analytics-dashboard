"""
Analytics Engine — Productivity Score, Smart Insights, and Weekly Summaries
This module contains all the logic-based analytics for the Personal Analytics Dashboard.
"""

def calculate_productivity_score(study_hours, screen_time, mood_score):
    """
    Productivity Score Formula:
        raw = (study_hours / (screen_time + 1)) * mood_score
    Normalized to 0–100 using a cap of 15 for the raw score.
    """
    raw_score = (study_hours / (screen_time + 1)) * mood_score
    # Normalize: assume max raw score ~15, cap at 100
    normalized = min(round((raw_score / 15) * 100, 1), 100)
    return normalized


def generate_smart_insights(logs):
    """
    Generate dynamic, rule-based insights from user's daily logs.
    Returns a list of insight strings with emoji.
    """
    if not logs:
        return ["📭 No data available yet. Start logging your days to get insights!"]

    insights = []
    total_study = sum(log.study_hours for log in logs)
    total_screen = sum(log.screen_time_hours for log in logs)
    avg_mood = sum(log.mood_score for log in logs) / len(logs)
    avg_study = total_study / len(logs)
    avg_screen = total_screen / len(logs)

    # --- Rule 1: Screen time vs Study time ---
    if total_screen > total_study:
        insights.append("📱 High screen time is affecting your productivity. Try to reduce it.")
    else:
        insights.append("✅ Great job! Your study time is higher than your screen time.")

    # --- Rule 2: Mood check ---
    if avg_mood < 5:
        insights.append("😔 Low mood detected. Consider taking breaks and doing things you enjoy.")
    elif avg_mood >= 7:
        insights.append("😊 You've been in great spirits! Positive mood boosts productivity.")

    # --- Rule 3: Study consistency (trend over last days) ---
    if len(logs) >= 3:
        recent = logs[:3]  # Most recent 3 logs (already sorted desc)
        # Check if study hours are increasing (recent[0] > recent[1] > recent[2])
        if recent[0].study_hours > recent[1].study_hours > recent[2].study_hours:
            insights.append("📈 Great improvement in study consistency! Keep it up.")
        elif recent[0].study_hours < recent[1].study_hours < recent[2].study_hours:
            insights.append("📉 Your study hours are declining. Try to get back on track.")

    # --- Rule 4: Excellent focus ---
    if avg_study > 5:
        insights.append("🎯 Excellent focus level — averaging over 5 study hours/day!")

    # --- Rule 5: Productivity score insight ---
    scores = [calculate_productivity_score(l.study_hours, l.screen_time_hours, l.mood_score) for l in logs]
    avg_score = sum(scores) / len(scores) if scores else 0
    if avg_score >= 70:
        insights.append("🏆 Your productivity score is outstanding! You're a top performer.")
    elif avg_score < 40:
        insights.append("⚠️ Your productivity score is low. Balance study time and screen time.")

    return insights


def generate_weekly_summary(logs):
    """
    Generate a weekly summary with best/worst day, averages, and totals.
    Uses simple aggregation logic.
    """
    if not logs:
        return {
            "best_day": None,
            "worst_day": None,
            "avg_study_hours": 0,
            "avg_screen_time": 0,
            "avg_mood": 0,
            "total_study_hours": 0,
            "total_screen_time": 0,
            "total_logs": 0
        }

    best_day = max(logs, key=lambda l: l.study_hours)
    worst_day = min(logs, key=lambda l: l.study_hours)
    
    total_study = sum(l.study_hours for l in logs)
    total_screen = sum(l.screen_time_hours for l in logs)
    avg_mood = sum(l.mood_score for l in logs) / len(logs)

    return {
        "best_day": {
            "date": best_day.date.isoformat() if best_day.date else None,
            "study_hours": best_day.study_hours,
            "mood": best_day.mood_score
        },
        "worst_day": {
            "date": worst_day.date.isoformat() if worst_day.date else None,
            "study_hours": worst_day.study_hours,
            "mood": worst_day.mood_score
        },
        "avg_study_hours": round(total_study / len(logs), 2),
        "avg_screen_time": round(total_screen / len(logs), 2),
        "avg_mood": round(avg_mood, 1),
        "total_study_hours": round(total_study, 2),
        "total_screen_time": round(total_screen, 2),
        "total_logs": len(logs)
    }
