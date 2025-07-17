import os
import sys
from dotenv import load_dotenv
import streamlit as st

# Extend system path for module resolution
sys.path.append(os.path.abspath(".."))

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("⚠️ GEMINI_API_KEY is missing in the .env file.")

# External Dependencies
from agents import (
    Agent, AsyncOpenAI, OpenAIChatCompletionsModel,
    RunConfig, handoff, InputGuardrailTripwireTriggered
)
from agentss.escalation_agent import (
    escalation_agent, EscalationReason, on_escalation_handoff
)
from agentss.nutrition_expert_agent import nutrition_expert_agent
from agentss.injury_support_agent import injury_support_agent
from context import UserSessionContext
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import meal_planner_tool
from tools.workou_recommender import workout_recommender_tool
from tools.scheduler import checkin_scheduler_tool
from tools.tracker import progress_tracker_tool

# Set up external model client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Configure the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Initialize user session context
user_context = UserSessionContext(
    name="shasmeen zahra",
    uid=123,
)

# Define the core agent
get_health_agent = Agent(
    name="Smart Health Planner 🧠💪",
    instructions="""
You are a proactive health and wellness assistant.

Your role:
- Understand the user’s fitness, nutrition, and wellness goals.
- Remember context from past interactions.
- Recommend personalized actions using available tools.

Handoff criteria:
- Mention of injuries (e.g. sprain, fracture, pain) → `injury_support`
- Mention of specific dietary needs (e.g. diabetic, keto, allergies) → `nutrition_expert`
- Request for human interaction → escalate via `escalation`

Once a handoff is triggered, do NOT respond yourself — allow the assigned agent to take over.
""",
    tools=[
        analyze_goal,
        meal_planner_tool,
        workout_recommender_tool,
        checkin_scheduler_tool,
        progress_tracker_tool,
    ],
    handoffs={
        "injury_support": injury_support_agent,
        "nutrition_expert": nutrition_expert_agent,
        "escalation": handoff(
            agent=escalation_agent,
            input_type=EscalationReason,
            on_handoff=on_escalation_handoff
        ),
    },
)

# ─────────────────────────────────────
# 📱 USER INTERFACE SECTION
# ─────────────────────────────────────

# Set layout & styles
st.set_page_config(
    page_title="Smart Health Planner 🧠",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f8;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    h1, h2, h3 {
        color: #1f2937;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("👋 Hello, Shasmeen!")
st.subheader("Welcome to your **Smart Health Planner** 💪🌿")
st.write("Track your fitness goals, plan your meals, get injury support, and more — all in one place.")

# Quick Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Weight", "58kg", "-2kg")
with col2:
    st.metric("Goal Progress", "70%", "📈")
with col3:
    st.metric("Meal Plans Created", "12", "+3")

st.markdown("---")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🎯 Fitness Goals", "🍽️ Meal Planner", "📅 Schedule"])

# Fitness Goals Tab
with tab1:
    st.header("🎯 Define Your Goal")
    goal_text = st.text_input("Enter a goal like: 'Lose 5kg in 2 months'")
    if goal_text:
        try:
            result = st.session_state.get("goal_result") or analyze_goal(user_context, goal_text)
            st.session_state["goal_result"] = result
            st.success("✅ Goal accepted and validated!")
            st.json(result)
        except Exception as e:
            st.error(f"❌ {str(e)}")

    st.subheader("🏃 Workout Tips")
    st.write("• 30 mins cardio daily")
    st.write("• 3x strength training weekly")
    st.write("• Hydrate regularly 🥤")

# Meal Planner Tab
with tab2:
    st.header("🍎 Choose Your Diet Plan")
    diet = st.selectbox("Select your dietary type", ["Balanced", "Keto", "Vegetarian", "Diabetic"])
    st.write(f"📋 Recommended Meals for **{diet}**:")

    st.write("- 🥣 Breakfast: Oats with fruits")
    st.write("- 🥗 Lunch: Grilled protein + veggies")
    st.write("- 🍲 Dinner: Light soup + salad")

# Schedule Tab
with tab3:
    st.header("📅 Weekly Check-In")
    st.date_input("📍 Choose your next check-in date")
    st.write("📝 Remember: Weekly tracking helps you stay on top!")

# Footer
st.markdown("---")
with st.expander("💬 Need Help?"):
    st.write("- 🩺 Talk to Injury Support Agent")
    st.write("- 🍎 Ask the Nutrition Expert")
    st.write("- 🙋 Escalate to a human if needed")

st.markdown("<center><sub>Made with ❤️ by Shasmeen</sub></center>", unsafe_allow_html=True)
