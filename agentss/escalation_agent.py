from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, AgentHooks, RunContextWrapper
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from pydantic import BaseModel


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

class EscalationReason(BaseModel):
    reason: str

async def on_escalation_handoff(ctx: RunContextWrapper, input_data: EscalationReason):
    reason = input_data.reason
    print(f"📢 Escalation triggered. Reason: {reason}")

    if hasattr(ctx.context, "handoff_logs") and isinstance(ctx.context.handoff_logs, list):
        ctx.context.handoff_logs.append(f"Escalation triggered: {reason}")
    else:
        ctx.context.handoff_logs = [f"Escalation triggered: {reason}"]

escalation_agent = Agent(
    name="Escalation Agent", 
    instructions="You are a human coach. If the user wants to speak to a human, you will assist them in doing so. If they ask for help, you will provide guidance and support as a human coach would.",
    model=model)


print("escalation agent Loaded")