def get_current_question(questions, index):
    """Returns the question at the given index, or None if finished."""
    if 0 <= index < len(questions):
        return questions[index]
    return None

def is_session_complete(questions, index):
    return index >= len(questions)