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
import sys
import os
sys.path.append(os.path.abspath(".."))
from context import UserSessionContext
from agents.run import RunConfig
from dotenv import load_dotenv
import os

class MealPlanOutput(BaseModel):
    diet_preferences: str
    meal_plan: List[str]

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


MealPlannerAgent = Agent(
    name="Meal Planner Agent",
    instructions="""
You are a meal planning expert. Given a user's dietary preference (e.g., vegetarian, keto, diabetic),
generate a 7-day meal plan in list format. Also return the diet type in your response.
""",
    output_type=MealPlanOutput,
    model=model
)

@function_tool
async def meal_planner_tool(context: RunContextWrapper[UserSessionContext], meal_text: str) -> dict:
    """
    Uses MealPlannerAgent to generate a structured 7-day meal plan from dietary preference input.
    """

    result = await Runner.run(
        MealPlannerAgent,
        meal_text,
        context=context.context,
        run_config=config
    )

    structured_output = result.final_output

    context.context.meal_plan = structured_output.meal_plan
    context.context.diet_preferences = structured_output.diet_preferences

    return {
        "diet_preferences": structured_output.diet_preferences,
        "meal_plan": structured_output.meal_plan
    }
