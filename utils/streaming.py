# import streamlit as st
# import os
# import asyncio
# from dotenv import load_dotenv
# import sys
# sys.path.append(os.path.abspath(".."))  
# from context import UserSessionContext
# from agents import Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig
# from agent import get_health_agent
# from datetime import datetime

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# external_client = AsyncOpenAI(
#     api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )

# st.set_page_config(page_title="Health Assistant", page_icon="💬")
# st.title("💬 Health & Wellness AI Assistant")

# def initialize_user_context():
#     return UserSessionContext(
#         name="Muniza",
#         uid=122
#     )

# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# if "user_context" not in st.session_state:
#     st.session_state["user_context"] = initialize_user_context()

# user_context = st.session_state["user_context"]

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# user_input = st.chat_input("Say something...")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     with st.chat_message("assistant"):
#         placeholder = st.empty()

#         async def stream_response():
#             response = ""
#             chat_history = ""
#             for m in st.session_state.messages:
#                 role = m["role"].capitalize()
#                 chat_history += f"{role}: {m['content']}\n"

#             full_prompt = f"{chat_history}User: {user_input}"

#             result = Runner.run_streamed(
#                 get_health_agent,
#                 full_prompt,
#                 run_config=config,
#                 context=user_context
#             )

#             async for event in result.stream_events():
#                 if event.type == "tool_call_event":
#                     tool_name = event.tool_call.tool_name
#                     tool_msg = f"🛠 Tool called: `{tool_name}`"
#                     placeholder.markdown(tool_msg)
#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": tool_msg
#                     })

#                 elif event.type == "raw_response_event" and hasattr(event.data, "delta"):
#                     token = event.data.delta
#                     response += token
#                     placeholder.markdown(response)

#             return response

#         final_output = asyncio.run(stream_response())
#         st.session_state.messages.append({"role": "assistant", "content": final_output})

# if user_context.handoff_logs:
#     st.sidebar.markdown("### 🧾 Handoff Logs")
#     for log in user_context.handoff_logs:
#         st.sidebar.markdown(f"- {log}")


# -------------



import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(".."))  
from context import UserSessionContext
from agents import Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agent import get_health_agent
from datetime import datetime

def run_streaming_ui():
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

    st.set_page_config(page_title="Health Assistant")


    st.write("Health Agent Chat")

    st.title("")
    st.title("")
    st.write("")

    st.markdown(
            "<h1 style='text-align: center;'>Health & Wellness Planner</h1>",
            unsafe_allow_html=True
        )

    def initialize_user_context():
        return UserSessionContext(name="Muniza", uid=122)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "user_context" not in st.session_state:
        st.session_state["user_context"] = initialize_user_context()

    user_context = st.session_state["user_context"]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
        
    user_input = st.chat_input("Say something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()

            async def stream_response():
                response = ""
                chat_history = ""
                for m in st.session_state.messages:
                    role = m["role"].capitalize()
                    chat_history += f"{role}: {m['content']}\n"

                full_prompt = f"{chat_history}User: {user_input}"

                result = Runner.run_streamed(
                    get_health_agent,
                    full_prompt,
                    run_config=config,
                    context=user_context
                )

                async for event in result.stream_events():
                    if event.type == "tool_call_event":
                        tool_name = event.tool_call.tool_name
                        tool_msg = f"🛠 Tool called: `{tool_name}`"
                        placeholder.markdown(tool_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": tool_msg
                        })
                    elif event.type == "raw_response_event" and hasattr(event.data, "delta"):
                        token = event.data.delta
                        response += token
                        placeholder.markdown(response)

                return response

            final_output = asyncio.run(stream_response())
            st.session_state.messages.append({"role": "assistant", "content": final_output})

    if user_context.handoff_logs:
        st.sidebar.markdown("### 🧾 Handoff Logs")
        for log in user_context.handoff_logs:
            st.sidebar.markdown(f"- {log}")

    