from orchestrator import call_gemini
from storage import load_data, save_data

from security_utils import sanitize_input

def set_goal(role, timeline, focus_areas):
    role = sanitize_input(role)
    timeline = sanitize_input(timeline)
    focus_areas = sanitize_input(focus_areas)

    data = load_data()
    data["goal"] = {
        "role": role,
        "timeline": timeline,
        "focus_areas": focus_areas
    }
    save_data(data)
   

def set_goal(role, timeline, focus_areas):
    """
    Saves the user's goal to local storage.
    Also asks Gemini to produce a short structured summary/confirmation.
    """
    data = load_data()
    data["goal"] = {
        "role": role,
        "timeline": timeline,
        "focus_areas": focus_areas
    }
    save_data(data)

    prompt = f"""
    The user has set this interview prep goal:
    Role: {role}
    Timeline: {timeline}
    Focus areas: {focus_areas}

    Write a brief, encouraging 2-sentence confirmation summarizing their goal.
    """
    summary = call_gemini(prompt)
    return summary

def get_goal():
    data = load_data()
    return data.get("goal", {})