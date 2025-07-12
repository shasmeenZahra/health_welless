from pydantic import BaseModel
from typing import List
from agents import (
    Agent,
    function_tool,
    RunContextWrapper,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel
)
import os
import sys
sys.path.append(os.path.abspath("..")) 
from context import UserSessionContext
from agents.run import RunConfig
from dotenv import load_dotenv

class WorkoutPlanOutput(BaseModel):
    workout_plan: List[str]

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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

WorkoutPlannerAgent = Agent(
    name="Workout Planner Agent",
    instructions="""
You are a workout planning expert. Based on a user's fitness goal and experience level, 
generate a weekly structured workout plan. 
Return a list of 7 workouts (one per day).
""",
    output_type=WorkoutPlanOutput,
    model=model
)
@function_tool
async def workout_recommender_tool(
    context: RunContextWrapper[UserSessionContext]
) -> dict:
    """
    Uses WorkoutPlannerAgent to generate a structured workout plan
    based on the user's goal saved in the session context.
    """

    print("💥 workout_recommender_tool was called!") 


    goal_data = context.context.goal

    if not goal_data:
        raise ValueError("No fitness goal found in context.")

    goal_text = f"{goal_data['goal_type']} {goal_data['quantity']} {goal_data['metric']} in {goal_data['duration']}"

    result = await Runner.run(
        WorkoutPlannerAgent,
        goal_text,
        context=context.context,
        run_config=config
    )

    structured_output = result.final_output

    context.context.workout_plan = structured_output.workout_plan

    return {
        "workout_plan": structured_output.workout_plan
    }
