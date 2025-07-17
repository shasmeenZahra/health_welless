```markdown
# 🏋️ Health & Wellness Planner Agent

An intelligent health assistant powered by **Gemini API** and **OpenAI Agents SDK**, designed to help you stay fit, eat better, and track your progress — all with a natural chat experience.

---

## ✨ Features

- ✅ **Goal analysis** with smart parsing (`e.g. lose 5kg in 2 months`)
- ✅ **7-day meal planner** tailored to your needs
- ✅ **Workout recommendations** based on your goal type
- ✅ **Weekly check-in scheduling**
- ✅ **Progress tracker**
- ✅ **Real-time streaming chat UI (Streamlit)**
- ✅ **Automatic handoffs to specialized agents**:
  - Injury support 🦵
  - Nutrition expert 🥦
  - Human escalation 👩‍⚕️

---

## 📁 Project Structure

```

health-and-wellness-planner-agent/
├── main.py                      # Streamlit entry point

├── agent.py                     # Main health agent and handoff logic

├── config.py                    # API key & model setup

├── context.py                   # User session context class

├── guardrails.py                # Input/output validation logic

├── hooks.py                     # Hooks (e.g. startup logic)

├── tools/

│   ├── goal\_analyzer.py         # Goal parsing logic

│   ├── meal\_planner.py          # Meal planner tool

│   ├── progress\_tracker.py      # Tracks progress & updates context

│   ├── workout\_recommender.py   # Suggests personalized workouts

│   └── scheduler.py             # Weekly check-in logic

└── agentss/

├── injury\_support\_agent.py

├── nutrition\_expert\_agent.py

└── escalation\_agent.py

````

---

## 🚀 Getting Started

### 1. Clone the repository:

```bash
git clone https://github.com/shasmeenZahra/health_welless.git
cd health_wellness
````

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 🧠 Running the App

Start the Streamlit app:

```bash
streamlit run main.py
```

⚠️ Do **not** use `python main.py` — only run via Streamlit.

---

## 💬 Example Interactions

| 📝 User Input                             | 🤖 Agent Response                              |
| ----------------------------------------- | ---------------------------------------------- |
| I want to lose 5kg in 2 months            | Parses and plans workouts, meals, schedule     |
| I have diabetes — meal plan?              | Hands off to NutritionExpertAgent              |
| I hurt my knee — recommend safe exercises | Switches to InjurySupportAgent                 |
| I want to talk to a real person           | Escalates to a human coach via EscalationAgent |

---

## 🔧 Tools Used

| Tool Name                  | Purpose                              |
| -------------------------- | ------------------------------------ |
| `analyze_goal`             | Parses goal into structured format   |
| `meal_planner_tool`        | Generates weekly meal plan           |
| `workout_recommender_tool` | Suggests exercises                   |
| `progress_tracker_tool`    | Logs progress and updates context    |
| `checkin_scheduler_tool`   | Creates weekly accountability checks |

---

## 🚦 Agent Handoffs

These are triggered by input patterns:

| Trigger Phrase                   | Agent Called         |
| -------------------------------- | -------------------- |
| "I have diabetes/allergy"        | NutritionExpertAgent |
| "I hurt my knee/back"            | InjurySupportAgent   |
| "I want to talk to a real coach" | EscalationAgent      |

---

## 🧠 Architecture Overview

```
User Input → Main Health Agent
    ├── Check for injuries, diet needs, or escalation
    ├── If handoff needed → Route to specialized agent
    ├── Else → Call appropriate tool
    └── Stream response back to user (via Streamlit)
```

---

## 🛠 Developer Notes

* Modify tools in `tools/`, then import in `main.py`
* Create new agents in `agentss/` and register in `agent.py`
* All context (e.g. goal type) is tracked in `context.py`
* Real-time streaming handled in `streamlit.run_agent_response()`

---

## 📜 License

Built with ❤️ by Shasmeen Zahra using OpenAI Agents SDK, Gemini API, and Streamlit.

---

## 🗣️ Feedback

Found a bug or want to contribute? Feel free to submit a pull request or open an issue.
