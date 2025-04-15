import os
import streamlit as st
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LLM_PROVIDER = "OPENAI"

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

if LLM_PROVIDER == "OPENAI":
    from openai import OpenAI
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
    )

elif LLM_PROVIDER == "ANTHROPIC":
    import anthropic
    client = anthropic.Anthropic(
        api_key=st.secrets["ANTHROPIC_API_KEY"],
        )

elif LLM_PROVIDER == "GOOGLE":
    from google import genai
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Function to interact with LLM
def generate_response(user_input, relevant_context, llm_proivder = LLM_PROVIDER):
    try:
        if LLM_PROVIDER == "OPENAI":

            # #find out which files to load
            # chat_completion = client.chat.completions.create(
            #       model="gpt-4o-mini",
            #       messages=[
            #         {
            #           "role": "system",
            #           "content": [
            #             {
            #               "type": "text",
            #               "text": relevant_context}
            #           ]
            #         },
            #         {
            #           "role": "user",
            #           "content": [
            #             {
            #               "type": "text",
            #               "text": "Lookup file names in the provided table to see \
            #               which files have recipes relevant to following question \
            #               and return the file names as a Python list:" + f"'{user_input}'"
            #             }
            #           ]
            #         }
            #       ],
            #       temperature=1,
            #       max_completion_tokens=2048,
            #       top_p=1,
            #       frequency_penalty=0,
            #       presence_penalty=0
            #       )
            #
            # first_response = chat_completion.choices[0].message.content
            # start = first_response.find('[')
            # end = first_response.find(']') + 1
            # first_response = first_response[start:end]
            # print("First response:")
            # first_response

            #load salient files
<<<<<<< HEAD
            salient_files = ["data/Week_of_August_25th_2024.txt", "data/Week_of_January_12th_2025.txt", "data/Week_of_June_23rd_2024.txt", "data/Week_of_September_22nd_2024.txt"]
=======
            salient_files = ["data/Week_of_December_15th_2024.txt", "data/Week_of_November_3rd_2024.txt", "data/Week_of_August_25th_2024.txt", "data/Week_of_November_17th_2024.txt"]
>>>>>>> f9c3d50d962a7cfd68695658d43a998d7c740f68
            relevant_context = relevant_context + salient_recipes (salient_files)

            #ask user question
            chat_completion = client.chat.completions.create(
                  model="gpt-4o-mini",
                  messages=[
                    {
                      "role": "system",
                      "content": [
                        {
                          "type": "text",
                          "text": relevant_context}
                      ]
                    },
                    {
                      "role": "user",
                      "content": [
                        {
                          "type": "text",
                          "text": user_input
                        }
                      ]
                    }
                  ],
                  temperature=1,
                  max_completion_tokens=2048,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                  )
            return chat_completion.choices[0].message.content

            messages = prompt.invoke({"question": user_input, "context": relevant_context + "/n" + docs_content})
            response = llm.invoke(messages)
            return response.content
        elif LLM_PROVIDER == "ANTHROPIC":
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1024,
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
        elif LLM_PROVIDER == "GOOGLE":
            response = client.models.generate_content(
                model="gemini-2.0-flash", #gemini-1.5-pro
                contents=relevant_context + user_input
            )
            return response.text
    except Exception as e:
        print (e)
        return


# Streamlit App
import streamlit as st
st.set_page_config(
    page_title="Meal prep assistant",
    page_icon="👨‍🍳"  # You can use an emoji or a file path to an image
)
st.title("Meal prep assistant")
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
