import streamlit as st

# ─────────────────────────────────────
# 🎨 PAGE CONFIGURATION + STYLING
# ─────────────────────────────────────
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

# ─────────────────────────────────────
# 🧠 HEADER
# ─────────────────────────────────────
st.title("👋 Hello, Shasmeen!")
st.subheader("Welcome to your **Smart Health Planner** 💪🌿")
st.write("Track your fitness goals, plan your meals, get injury support, and more — all in one place.")

# ─────────────────────────────────────
# 📊 METRICS / QUICK STATS
# ─────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Weight", "58kg", "-2kg")
with col2:
    st.metric("Goal Progress", "70%", "📈")
with col3:
    st.metric("Meal Plans Created", "12", "+3")

st.markdown("---")

# ─────────────────────────────────────
# 🗂️ MAIN CONTENT TABS
# ─────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏋️‍♀️ Fitness Goals", "🍽️ Meal Planner", "📅 Schedule"])

# --- FITNESS TAB ---
with tab1:
    st.header("🎯 Your Goal")
    st.write("Example: *Lose 5kg in 2 months*")
    goal_input = st.text_input("Enter your goal:")

    if goal_input:
        st.success(f"Goal received: **{goal_input}** (validated ✅)")

    st.subheader("🏃 Recommended Workouts")
    st.write("• 30 mins cardio daily\n• 3x full-body strength per week")

# --- MEAL PLANNER TAB ---
with tab2:
    st.header("🥗 Personalized Meal Plan")
    st.write("Select your dietary preference:")
    diet = st.selectbox("Diet Type", ["Balanced", "Keto", "Vegetarian", "Diabetic-friendly"])
    
    if diet:
        st.success(f"You selected a **{diet}** diet. Here's your sample meal plan:")
        st.write("- 🥣 Breakfast: Greek Yogurt with Berries")
        st.write("- 🥗 Lunch: Grilled Chicken + Veggies")
        st.write("- 🍲 Dinner: Lentil Soup + Brown Rice")

# --- SCHEDULE TAB ---
with tab3:
    st.header("📅 Check-In Schedule")
    st.date_input("Next Check-In Date")
    st.write("💡 Tip: Weekly check-ins help track your progress effectively.")

st.markdown("---")

# ─────────────────────────────────────
# 💬 FOOTER / SUPPORT
# ─────────────────────────────────────
with st.expander("💬 Need Help?"):
    st.write("Talk to:")
    st.write("- 🩺 Injury Support Agent")
    st.write("- 🍎 Nutrition Expert")
    st.write("- 🙋 Escalation Assistant (human support)")

st.markdown("<center><sub>Made with ❤️ by Shasmeen</sub></center>", unsafe_allow_html=True)
