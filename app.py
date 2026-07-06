import streamlit as st
from goal_setter_agent import set_goal, get_goal
from question_generator_agent import generate_questions
from mock_interviewer_agent import get_current_question, is_session_complete
from security_utils import is_suspicious

st.title("AI Interview Prep Assistant")
from dashboard_agent import get_dashboard_data
import pandas as pd

st.header("🏠 Today's Dashboard")

dash = get_dashboard_data()

col1, col2, col3 = st.columns(3)
col1.metric("🔥 Streak", f"{dash['streak']} days")
col2.metric("📅 Sessions Completed", dash["total_sessions"])
col3.metric("🎯 Focus Area", dash["top_weak_area"].replace("_", " ") if dash["top_weak_area"] else "None yet")

if dash["goal"]:
    st.write(f"**Current goal:** {dash['goal'].get('role')} — {dash['goal'].get('timeline')}")

if dash["score_trend"]:
    st.subheader("📈 Score Trend")
    df = pd.DataFrame(dash["score_trend"])
    st.line_chart(df.set_index("session"))

from storage import reset_data

with st.sidebar:
    st.subheader("⚙️ Settings")
    if st.button("🗑️ Reset All Progress"):
        reset_data()
        st.session_state.clear()
        st.success("All progress cleared!")
        st.rerun()
st.divider()
# --- Step 3: Goal Setup ---
st.header("🎯 Set Your Goal")

existing_goal = get_goal()
if existing_goal:
    st.info(f"Current goal: {existing_goal.get('role')} — {existing_goal.get('timeline')}")

role = st.text_input("Target role", value=existing_goal.get("role", ""))
timeline = st.text_input("Timeline (e.g. 4 weeks)", value=existing_goal.get("timeline", ""))
focus_areas = st.text_input("Focus areas (comma-separated)", value=existing_goal.get("focus_areas", ""))

if st.button("Save Goal"):
    if role and timeline:
        summary = set_goal(role, timeline, focus_areas)
        st.success("Goal saved!")
        st.write(summary)
    else:
        st.warning("Please fill in at least role and timeline.")

# --- Step 4: Question Generator ---
st.header("📝 Today's Questions")

if st.button("Generate Questions"):
    goal = get_goal()
    if goal:
        questions = generate_questions()
        st.session_state["questions"] = questions
        # Reset all previous session state so old interview doesn't linger
        st.session_state["current_index"] = 0
        st.session_state["answers"] = []
        st.session_state["session_scored"] = False
        st.session_state.pop("session_results", None)
        for i, q in enumerate(questions, 1):
            st.write(f"{i}. {q}")
    else:
        st.warning("Please set your goal first.")

# --- Step 5: Mock Interviewer ---
st.header("🎤 Mock Interview")

if "questions" in st.session_state:
    if "current_index" not in st.session_state:
        st.session_state["current_index"] = 0
    if "answers" not in st.session_state:
        st.session_state["answers"] = []

    idx = st.session_state["current_index"]
    questions = st.session_state["questions"]

    if not is_session_complete(questions, idx):
        current_q = get_current_question(questions, idx)
        st.subheader(f"Question {idx + 1} of {len(questions)}")
        st.write(current_q)

        answer = st.text_area("Your answer:", key=f"answer_{idx}")
        if answer and is_suspicious(answer):
            st.warning("⚠️ Your answer contains unusual instruction-like phrases and will be sanitized before processing.")
        if st.button("Submit Answer"):
            if answer:
                st.session_state["answers"].append({"question": current_q, "answer": answer})
                st.session_state["current_index"] += 1
                st.rerun()
            else:
                st.warning("Please type an answer before submitting.")
    else:
        st.success("🎉 Mock interview session complete!")

        if "session_scored" not in st.session_state or not st.session_state["session_scored"]:
            with st.spinner("Scoring your answers..."):
                from feedback_coach_agent import score_session
                results = score_session(st.session_state["answers"])
                st.session_state["session_results"] = results
                st.session_state["session_scored"] = True
            st.rerun()

        st.subheader("📊 Your Results")
        for i, r in enumerate(st.session_state["session_results"], 1):
            st.write(f"**Q{i}: {r['question']}**")
            st.write(f"Overall: {r['overall_score']}/10 | Clarity: {r['clarity']} | Structure: {r['structure']} | Relevance: {r['relevance']} | Confidence: {r['confidence']}")
            st.write(f"💬 {r['one_line_feedback']}")
            st.divider()
else:
    st.info("Generate questions above to start your mock interview.")

from study_planner_agent import suggest_study_resources

st.header("📚 Study Recommendations")

if st.button("Get Study Resources"):
    with st.spinner("Searching for relevant resources..."):
        resources, weak_area = suggest_study_resources()

    if weak_area:
        st.write(f"Based on your weak area: **{weak_area.replace('_', ' ')}**")
    else:
        st.write("General resources for your target role:")

    for r in resources:
        st.markdown(f"- [{r['title']}]({r['url']})")