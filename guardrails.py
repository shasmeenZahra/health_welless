# 📦 Required libraries import kar rahe hain
import os  # system environment variables ke liye
from dotenv import load_dotenv  # .env file se API key load karne ke liye
from pydantic import BaseModel  # data validation ke liye (like input/output format check)

# 🧠 AI-related tools import kar rahe hain
from agents import (
    Agent,  # AI agent banane ke liye
    GuardrailFunctionOutput,  # Guardrail ka result handle karne ke liye
    RunContextWrapper,  # context pass karne ke liye
    Runner,  # agent run karne ke liye
    TResponseInputItem,  # input type define karne ke liye
    input_guardrail,  # input check karne wala decorator
    output_guardrail,  # output check karne wala decorator
    AsyncOpenAI,  # OpenAI client (Gemini yahan use ho raha)
    OpenAIChatCompletionsModel,  # Chat model use karne ke liye
    RunConfig,  # model configuration ke liye
)
# ─────────────────────────────────────────────
# Load environment and initialize model config
# ─────────────────────────────────────────────
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("🔐 GEMINI_API_KEY environment variable is not set.")

openai_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

chat_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=openai_client,
)

llm_config = RunConfig(
    model=chat_model,
    model_provider=openai_client,
    tracing_disabled=True
)

# ──────────────────────────────
# Weight Goal Validation Models
# ──────────────────────────────
class WeightGoalData(BaseModel):
    is_goal_valid: bool
    quantity: str
    metric: str
    duration: str

class WeightGoalResponse(BaseModel):
    is_goal_valid: bool
    response: str

# ──────────────────────────────────────────────────
# Weight Goal Guardrail Agents: Input & Output Check
# ──────────────────────────────────────────────────
weight_goal_input_validator = Agent(
    name="WeightGoalInputValidator",
    instructions="""
Check if the input includes a realistic weight goal.
Examples include: 'lose 5kg in 2 months', 'gain 10 pounds in 6 weeks', etc.

Return:
{
  "is_goal_valid": true,
  "quantity": "5",
  "metric": "kg",
  "duration": "2 months"
}

If not valid or missing data:
{
  "is_goal_valid": false,
  "quantity": "",
  "metric": "",
  "duration": ""
}
""",
    output_type=WeightGoalData,
)

weight_goal_output_validator = Agent(
    name="WeightGoalOutputValidator",
    instructions="Validate if the assistant's response contains a clear and actionable weight goal.",
    output_type=WeightGoalResponse,
)

# ───────────────────────────────
# Weight Goal Guardrail Functions
# ───────────────────────────────
@input_guardrail
async def validate_weight_goal_input(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(weight_goal_input_validator, input, context=ctx.context, run_config=llm_config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_goal_valid,
    )

@output_guardrail
async def validate_weight_goal_output(
    ctx: RunContextWrapper,
    agent: Agent,
    output: WeightGoalResponse
) -> GuardrailFunctionOutput:
    result = await Runner.run(weight_goal_output_validator, output.response, context=ctx.context, run_config=llm_config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_goal_valid,
    )

# ───────────────────────────────
# Injury Validation Models
# ───────────────────────────────
class InjuryData(BaseModel):
    is_injury_valid: bool
    response: str

# ───────────────────────────────────────────────
# Injury Guardrail Agents: Input & Output Check
# ───────────────────────────────────────────────
injury_input_validator = Agent(
    name="InjuryInputValidator",
    instructions="""
Detect if the user's input describes an injury or requests injury support.

Examples: 'I sprained my ankle', 'My back hurts after the workout', etc.

Return:
{
  "is_injury_valid": true,
  "response": "<short summary of the injury>"
}

If irrelevant:
{
  "is_injury_valid": false,
  "response": ""
}
""",
    output_type=InjuryData,
)

injury_output_validator = Agent(
    name="InjuryOutputValidator",
    instructions="Validate if the assistant's output addresses a valid injury concern or support request.",
    output_type=InjuryData,
)

# ───────────────────────────────
# Injury Guardrail Functions
# ───────────────────────────────
@input_guardrail
async def validate_injury_input(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(injury_input_validator, input, context=ctx.context, run_config=llm_config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_injury_valid,
    )

@output_guardrail
async def validate_injury_output(
    ctx: RunContextWrapper,
    agent: Agent,
    output: InjuryData
) -> GuardrailFunctionOutput:
    result = await Runner.run(injury_output_validator, output.response, context=ctx.context, run_config=llm_config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_injury_valid,
    )
