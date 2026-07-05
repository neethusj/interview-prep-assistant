import json
import os

DATA_PATH = "data/user_data.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return {"goal": {}, "sessions": [], "weak_areas": {}, "study_log": [], "streak": 0}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def reset_data():
    fresh_data = {"goal": {}, "sessions": [], "weak_areas": {}, "study_log": [], "streak": 0}
    save_data(fresh_data)
    return fresh_data