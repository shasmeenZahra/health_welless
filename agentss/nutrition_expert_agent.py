from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
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

nutrition_expert_agent: Agent = Agent(name="Nutrition Expert Agent", instructions="You are a nutrition expert agent. You help users with dietary queries, meal planning, and nutritional advice. You can handle complex dietary needs like diabetes or allergies.", model=model)

print("Nutrition Expert Agent Loaded")  