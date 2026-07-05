import json
from orchestrator import call_gemini
from storage import load_data, save_data


from security_utils import sanitize_input

def score_answer(question, answer):
    question = sanitize_input(question)
    answer = sanitize_input(answer)
    


def score_answer(question, answer):
    """
    Scores a single Q&A pair across 4 dimensions (1-10 each) + overall.
    Returns a dict with scores, feedback, and identified weak area (if any).
    """
    prompt = f"""
    You are an interview coach. Score this answer.

    Question: {question}
    Answer: {answer}

    Score each dimension from 1-10:
    - Clarity
    - Structure (STAR method where applicable)
    - Relevance
    - Confidence

    Also give:
    - overall_score (1-10)
    - one_line_feedback (short, constructive)
    - weak_area (a short tag like "system_design", "behavioral_star", "communication", or null if none stands out)

    Return ONLY valid JSON, no markdown, in this exact format:
    {{
      "clarity": 0,
      "structure": 0,
      "relevance": 0,
      "confidence": 0,
      "overall_score": 0,
      "one_line_feedback": "",
      "weak_area": ""
    }}
    """
    response = call_gemini(prompt)
    clean = response.strip().replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {
            "clarity": 5, "structure": 5, "relevance": 5, "confidence": 5,
            "overall_score": 5, "one_line_feedback": "Could not parse detailed feedback.",
            "weak_area": None
        }

def score_session(answers):
    """
    Scores a full list of {question, answer} dicts.
    Updates weak_areas tracker and saves session to storage.
    """
    data = load_data()
    session_results = []

    
    for item in answers:
        clean_question = sanitize_input(item["question"])
        clean_answer = sanitize_input(item["answer"])

        result = score_answer(item["question"], item["answer"])
        result["question"] = clean_question
        result["answer"] = clean_answer
        session_results.append(result)

        weak = result.get("weak_area")
        if weak and weak.lower() != "null":
            data["weak_areas"][weak] = data["weak_areas"].get(weak, 0) + 1

    data["sessions"].append(session_results)
    data["streak"] = data.get("streak", 0) + 1
    save_data(data)

    return session_results