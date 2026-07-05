import os
from dotenv import load_dotenv
from tavily import TavilyClient
from storage import load_data, save_data

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_top_weak_area(data):
    """Returns the most frequent weak area, or None."""
    weak_areas = data.get("weak_areas", {})
    if not weak_areas:
        return None
    return max(weak_areas, key=weak_areas.get)

def suggest_study_resources(max_results=3):
    """
    Searches Tavily for study resources based on goal + top weak area.
    Logs results to storage and returns them.
    """
    data = load_data()
    goal = data.get("goal", {})
    role = goal.get("role", "Software Engineer")
    weak_area = get_top_weak_area(data)

    if weak_area:
        query = f"{role} interview preparation {weak_area.replace('_', ' ')} resources guide"
    else:
        query = f"{role} interview preparation guide common questions"

    response = tavily_client.search(query=query, max_results=max_results)
    results = response.get("results", [])

    resources = []
    for r in results:
        resource = {
            "title": r.get("title", "Untitled"),
            "url": r.get("url", ""),
            "topic": weak_area or "general",
            "done": False
        }
        resources.append(resource)
        data["study_log"].append(resource)

    save_data(data)
    return resources, weak_area