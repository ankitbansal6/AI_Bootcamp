import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


st.title("DataGPT")

st.write("Welcome to the data assistant")

user_input = st.text_input("ask your question")

if st.button("submit"):
    response = client.responses.create(model='gpt-5.6-sol',
                        input= user_input)

    result = response.output_text
    st.write(result)
