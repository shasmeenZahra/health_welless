from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig
)

from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

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

# class for input guardrail
class WeightGoalOutput(BaseModel):
    is_goal_valid: bool
    quantity: str
    metric: str
    duration: str

# class for output guardrail
class Goal_MessageOutput(BaseModel):
    is_goal_valid: bool
    response: str

input_goal_guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""
If the input includes a weight goal (like 'lose 5kg in 2 months'), return the following JSON:

{
  "is_goal_valid": true,
  "quantity": "5",
  "metric": "kg",
  "duration": "2 months",
}

If not valid, return:

{
  "is_goal_valid": false,
  "quantity": "",
  "metric": "",
  "duration": "",
}
""",
    output_type=WeightGoalOutput,
)


output_goal_guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if output is a valid weight goal. If so, extract the quantity, metric, and duration from the goal.",
    output_type=Goal_MessageOutput,
)


@input_guardrail
async def input_goal_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_goal_guardrail_agent, input, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_goal_valid,
    )


@output_guardrail
async def output_goal_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: Goal_MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_goal_guardrail_agent, output.response, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_goal_valid,
    )


# -----------------------------------------
# now Guardrails for injury support agent
# ------------------------------------------

# class for input and output guardrail
class InjuryOutput(BaseModel):
    is_injury_valid: bool
    response: str

input_injury_guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""
If the input includes a valid injury description or injury support request, return the following JSON:

{
  "is_injury_valid": true,
  "response": "<short summary of the injury or support needed>"
}

If not valid, return:

{
  "is_injury_valid": false,
  "response": ""
}
""",
    output_type=InjuryOutput,
)


output_meal_guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if output is a valid injury goal.",
    output_type=InjuryOutput,
)


@input_guardrail
async def input_injury_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_injury_guardrail_agent, input, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_injury_valid,
    )


@output_guardrail
async def output_injury_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: InjuryOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_meal_guardrail_agent, output.response, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_injury_valid,
    )
    

