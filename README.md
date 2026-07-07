# AI Interview Prep Assistant

A personal, multi-agent AI system that helps you prepare for job interviews — generates tailored questions, runs mock interview sessions, scores your answers, tracks your progress, and recommends real study resources.

Built for the 5-Day AI Agents: Intensive Vibe Coding Course with Google (Kaggle Capstone) — Concierge Agents track.

## Features

- 🎯 Goal setup (target role, timeline, focus areas)
- 📝 Tailored interview questions based on your goal and weak areas
- 🎤 Mock interview sessions (one question at a time)
- 📊 Scoring across Clarity, Structure, Relevance, and Confidence
- 📚 Real, live-sourced study resources via web search
- 🏠 Progress dashboard with streak and score trend chart
- 🔒 Input sanitization to guard against prompt injection
- All data stored locally — nothing leaves your machine except API calls to Gemini and Tavily

## Tech Stack

- Streamlit (UI)
- Gemini 2.5 Flash via google-genai SDK
- Tavily API (web search)
- Local JSON storage
- Python 3.12

## Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/neethusj/interview-prep-assistant.git
cd interview-prep-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your API keys

- **Gemini API key**: Go to [aistudio.google.com](https://aistudio.google.com) → API keys → create one (free tier)
- **Tavily API key**: Go to [tavily.com](https://tavily.com) → sign up → dashboard → copy your key (free tier)

### 4. Create a `.env` file in the project root

```
GEMINI_API_KEY=your_gemini_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Note on Data

This is a personal-use tool by design. All data (your goal, session history, scores, study log) is stored locally in `data/user_data.json` on your own machine — it is not shared or transmitted anywhere except the two required API calls to Gemini (for question generation/scoring) and Tavily (for study resource search).

## Project Structure

```
interview-prep-assistant/
├── app.py
├── orchestrator.py
├── storage.py
├── security_utils.py
├── goal_setter_agent.py
├── question_generator_agent.py
├── mock_interviewer_agent.py
├── feedback_coach_agent.py
├── study_planner_agent.py
├── dashboard_agent.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/user_data.json
```
