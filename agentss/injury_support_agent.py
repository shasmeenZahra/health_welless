from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, InputGuardrailTripwireTriggered
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import sys
import streamlit as st

# Add parent directory to import local guardrails module
sys.path.append(os.path.abspath(".."))

# ✅ FIXED: Corrected import names
from guardrails import validate_injury_input, validate_injury_output, InjuryData

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

# ✅ FIXED: Correct function and output_type
injury_support_agent: Agent = Agent(
    name="Injury support agent", 
    instructions="""You are an Injury Support Agent. Provide helpful, accurate, and empathetic advice to users seeking support for injuries. Always ensure your responses are safe, informative, and within your scope as an AI assistant. If a question is outside your expertise, advise the user to consult a healthcare professional.""",
    model=model,
    input_guardrails=[validate_injury_input],
    output_type=InjuryData,
    output_guardrails=[validate_injury_output]
)

print("Injury Support Agent Loaded")
