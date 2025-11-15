import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import langchain
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
import os
from dotenv import load_dotenv
load_dotenv()
langchain.debug = True
##Langsmith Tracking
os.environ['LANCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "default-project"
## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistance. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    genai.configure(api_key=api_key)
    llm = ChatGoogleGenerativeAI(model= llm, google_api_key=api_key)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer

st.title("ChatBot Q&A with gemini")
st.sidebar.title("Settings")
api_key = os.getenv("GEMINI_API_KEY")
llm = st.sidebar.selectbox("Select an Gemimi Model",["gemini-2.5-pro","gemini-2.5-flash","gemini-2.5-flash-preview-09-2025"])
temperature = st.sidebar.slider("Temperature", min_value = 0.0, max_value= 1.0, value= 0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value = 50 , max_value = 300, value=150)

## Main Interface
st.write("Go ahead and ask the question")
user_input = st.text_input("You:")

if user_input:
    answer = generate_response(user_input,api_key,llm,temperature,max)
    st.write(answer)
else :
    st.write("Please ask the question")
