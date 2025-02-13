import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
LLAMA_API_KEY = os.environ.get("LLAMA_API_KEY")

llm = ChatGroq(temperature=0, groq_api_key=LLAMA_API_KEY, model_name="llama3-8b-8192")

conversation_history = {"athlete": [], "coach": []}


def get_response(user_input, role):
    full_context = (
        "\n".join(conversation_history[role])
        + f"\nUser: {user_input}\nPlease respond briefly and factually as if you are advising a {role}. "
        f"Only provide accurate information based on facts. If you're unsure or there isn't enough information to give a complete answer, "
        f"ask the user for clarification or more details."
    )
    response = llm.invoke(full_context)

    conversation_history[role].append(f"{role.capitalize()}: {user_input}")
    conversation_history[role].append(f"Bot: {response.content}")

    return response.content


st.title("Athlix")

role = st.selectbox("Are you an Athlete or Coach?", ("athlete", "coach"))

user_input = st.text_input(f"{role.capitalize()}: ", "")

if st.button("Send"):
    if user_input:
        bot_response = get_response(user_input, role)

        st.markdown("### Conversation")
        for line in conversation_history[role]:
            if "Bot:" in line:
                st.write(f"**Bot:** {line.split('Bot: ')[-1]}")
            else:
                st.write(
                    f"**{role.capitalize()}:** {line.split(f'{role.capitalize()}: ')[-1]}"
                )

        st.markdown(f"**Bot:** {bot_response}")
