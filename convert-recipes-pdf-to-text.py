
import os
import streamlit as st

PDF_FOLDER="pdfs/"
TXT_FOLDER="data/"



# Get recipe content
from langchain_community.document_loaders import PyPDFLoader
files = [f for f in os.listdir(PDF_FOLDER) if not f.startswith('.')]
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

print("All done")
