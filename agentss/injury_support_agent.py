from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, InputGuardrailTripwireTriggered
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import sys
import streamlit as st
# for importing from the guardrails path because Python doesn’t automatically look in folders above the script unless you tell it to.
sys.path.append(os.path.abspath(".."))  
from guardrails import input_injury_guardrail, output_injury_guardrail, InjuryOutput

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

injury_support_agent: Agent = Agent(
    name="Injury support agent", 
    instructions="""You are an Injury Support Agent. Provide helpful, accurate, and empathetic advice to users seeking support for injuries. Always ensure your responses are safe, informative, and within your scope as an AI assistant. If a question is outside your expertise, advise the user to consult a healthcare professional.""",
    model=model,
    input_guardrails=[input_injury_guardrail],
    output_type=InjuryOutput,
    output_guardrails=[output_injury_guardrail]
    )

print("Injury Support Agent Loaded")