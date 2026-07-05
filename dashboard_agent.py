from storage import load_data

def get_dashboard_data():
    """
    Aggregates data for the Today dashboard.
    """
    data = load_data()
    streak = data.get("streak", 0)
    goal = data.get("goal", {})
    weak_areas = data.get("weak_areas", {})
    sessions = data.get("sessions", [])

    top_weak_area = max(weak_areas, key=weak_areas.get) if weak_areas else None

    # Build score trend: average overall_score per session
    score_trend = []
    for i, session in enumerate(sessions, 1):
        if session:
            avg = sum(r["overall_score"] for r in session) / len(session)
            score_trend.append({"session": i, "avg_score": round(avg, 1)})

    return {
        "streak": streak,
        "goal": goal,
        "top_weak_area": top_weak_area,
        "score_trend": score_trend,
        "total_sessions": len(sessions)
    }