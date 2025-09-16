import os
import streamlit as st
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LLM_PROVIDER = "ANTHROPIC"

# Tell the model today's date
from datetime import date
today = date.today()
relevant_context = f" Today's date is {today}. "

# Get system prompt
with open('meal-prep-assistant.md', 'r') as file:
    # Read the content of the file into a string variable
    relevant_context = relevant_context + file.read()
    file.close()

# Get salient recipes
def salient_recipes (file_paths):
    recipes = ""
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            # Read the content of the file into a string variable
            recipes = recipes + "/n" + file.read()
            file.close()
    return recipes

import anthropic
client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"],
)

# Function to interact with LLM
def generate_response(user_input, relevant_context):
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=[
              {
                "type": "text",
                "text": relevant_context,
                "cache_control": {"type": "ephemeral"}
              }
            ],
            messages=[
            {"role": "user", "content": user_input}
            ],
        )
        for content_block in message.content:
            if content_block.type == "text":
                text = content_block.text
        return text
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, I encountered an error while processing your request."


# Streamlit App
import streamlit as st
st.set_page_config(
    page_title="Meal prep assistant",
    page_icon="👨‍🍳"  # You can use an emoji or a file path to an image
)
st.title("Meal prep assistant")
st.warning("⚠️ **DEPRECATION NOTICE**: This product has been deprecated and is no longer actively maintained. Please consider migrating to alternative solutions.")
st.write("Ask me questions such as 'What is the meal plan for this week?' or 'What \
are the rally instructions for today?''")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    logger.info('{"event": "user_session_started"}')


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if input := st.chat_input("Message meal prep assistant"):
    # Display user message in chat message container
    st.chat_message("user").markdown(input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": input})
    # print (f"Question: {input}")
    response = generate_response(user_input=input, relevant_context=relevant_context)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        # print(f"Answer: {response}")
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
