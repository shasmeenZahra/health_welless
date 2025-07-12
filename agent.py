from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, handoff, InputGuardrailTripwireTriggered
from agentss.escalation_agent import escalation_agent, EscalationReason, on_escalation_handoff
import os
import sys
sys.path.append(os.path.abspath("..")) 
from context import UserSessionContext
from agentss.nutrition_expert_agent import nutrition_expert_agent
from agentss.injury_support_agent import injury_support_agent
import streamlit as st
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import meal_planner_tool
from tools.workou_recommender import workout_recommender_tool
from tools.scheduler import checkin_scheduler_tool
from tools.tracker import progress_tracker_tool
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please define it in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

user_context = UserSessionContext(
    name="Muniza",
    uid=122,
)
get_health_agent = Agent(
    name="Health Planner",
    instructions="""
You are a health and wellness assistant. You will receive the full chat history as part of the input.
Use this history to understand the user's goals, remember what they said previously, and respond accordingly.

Handoff rules:
- If the user mentions injury-related terms (sprain, pain, broken bone, hurt, accident, etc), trigger the `injury_support` handoff.
- If the user mentions special diet needs (diabetic, keto, allergies), use the `nutrition_expert` handoff.
- If the user says they want a human coach or real person, use the `escalation` handoff.

After handing off, don't answer yourself — the handed-off agent will respond.
""",
    tools=[analyze_goal, meal_planner_tool, workout_recommender_tool, checkin_scheduler_tool, progress_tracker_tool],
    handoffs={
        "injury_support": injury_support_agent,
        "nutrition_expert": nutrition_expert_agent,
        "escalation": handoff(
            agent=escalation_agent,
            input_type=EscalationReason,
            on_handoff=on_escalation_handoff,
        )
    },
)


