import json
from orchestrator import call_gemini
from storage import load_data

def generate_questions(num_questions=5):
    """
    Generates interview questions tailored to the user's goal and weak areas.
    Returns a list of question strings.
    """
    data = load_data()
    goal = data.get("goal", {})
    weak_areas = data.get("weak_areas", {})

    role = goal.get("role", "Software Engineer")
    focus_areas = goal.get("focus_areas", "general")
    weak_list = ", ".join(weak_areas.keys()) if weak_areas else "none identified yet"

    prompt = f"""
    Generate {num_questions} interview questions for a candidate preparing for this role:
    Role: {role}
    Focus areas: {focus_areas}
    Known weak areas from past sessions: {weak_list}

    Prioritize weak areas if any exist. Mix technical and behavioral questions as appropriate.

    Return ONLY a JSON array of strings, no markdown, no extra text. Example format:
    ["question 1", "question 2", "question 3"]
    """

    response = call_gemini(prompt)
    clean = response.strip().replace("```json", "").replace("```", "").strip()

    try:
        questions = json.loads(clean)
        return questions
    except json.JSONDecodeError:
        return [line.strip("- ") for line in response.split("\n") if line.strip()][:num_questions]