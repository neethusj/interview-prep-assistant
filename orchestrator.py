import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini(prompt, model="gemini-2.5-flash"):
    """Basic wrapper — every sub-agent will use this to talk to Gemini."""
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text

def route_request(user_input, current_step="goal_setup"):
    """
    Orchestrator entry point.
    For now just echoes back — in later steps this will call the right sub-agent.
    """
    if current_step == "goal_setup":
        return call_gemini(f"Acknowledge this interview prep goal briefly: {user_input}")
    return "Step not implemented yet."