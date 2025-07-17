from agents import (
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

# ✅ FIXED: Correct guardrail function names
from guardrails import validate_weight_goal_input, validate_weight_goal_output

from agents.run import RunConfig
from dotenv import load_dotenv
from pydantic import BaseModel
import re

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

class StructuredGoal(BaseModel):
    goal_type: str
    quantity: float
    metric: str
    duration: str

@function_tool
async def analyze_goal(context: RunContextWrapper[UserSessionContext], goal_text: str) -> dict:
    """
    Parses the goal and applies guardrails manually.
    """

    # ✅ FIXED: Use correct input guardrail
    input_check = await Runner.run(
        validate_weight_goal_input,
        goal_text,
        context=context.context,
        run_config=config
    )

    if not input_check.final_output.is_goal_valid:
        raise ValueError("Goal format is invalid (according to input guardrail).")

    weight_match = re.search(r"(lose|gain)\s+(\d+\.?\d*)\s*(kg|pounds|lbs)?", goal_text, re.I)
    duration_match = re.search(r"in\s+(\d+\s*(days|weeks|months|years))", goal_text, re.I)

    if not weight_match or not duration_match:
        raise ValueError("Missing weight or duration details.")

    action = weight_match.group(1).lower()
    quantity = float(weight_match.group(2))
    metric = weight_match.group(3) or "kg"
    duration = duration_match.group(1)

    structured = {
        "goal_type": "weight_loss" if action == "lose" else "weight_gain",
        "quantity": quantity,
        "metric": metric,
        "duration": duration
    }

    # ✅ FIXED: Use correct output guardrail
    output_check = await Runner.run(
        validate_weight_goal_output,
        f"{action} {quantity} {metric} in {duration}",
        context=context.context,
        run_config=config
    )

    if not output_check.final_output.is_goal_valid:
        raise ValueError("Output failed guardrail validation.")
    
    context.context.goal = structured

    return structured
