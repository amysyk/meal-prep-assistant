
import os
import streamlit as st

PDF_FOLDER="pdfs/"
TXT_FOLDER="data/"

from google import genai
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


# Get recipe content
from langchain_community.document_loaders import PyPDFLoader
files = [f for f in os.listdir(PDF_FOLDER) if not f.startswith('.')]
mapping = {}
print ("Files converted:")
for file in files:
    loader = PyPDFLoader(file_path = PDF_FOLDER + file, mode="single")

    for page in loader.lazy_load():
        text_file_path = TXT_FOLDER + file.split(".")[0] + ".txt"
        with open(text_file_path, "w") as file:
            #save as text
            file.write(page.page_content)
            file.close()
            print (text_file_path)
        mapping[text_file_path] = page.page_content[:500]

#generate meail to file mapping
from google import genai
response = client.models.generate_content(
    model = "gemini-2.0-flash", #gemini-1.5-pro
    contents = "The following key value pairs list file name and its summary.\
    Each summary includes four meals scheduled Monday through Thursday. Return \
    the data as raw markdown code for a table with two columns: file name and \
    meal. Each meal should be on its own row. Omit days of the week in meal names." + \
    "/n" + str(mapping)
)
with open(TXT_FOLDER + "file-to-meal-mapping.txt", "w") as file:
    #save as text
    file.write(response.text)
    file.close()

print("All done")
