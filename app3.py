import streamlit as st
from langchain_community.tools import DuckDuckGoSearchResults
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = api_key
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Talk2NetAssistAI 🛜")

search = DuckDuckGoSearchResults()

st.title("Talk2NetAssistAI 🛜")
st.markdown("It is an advanced chatbot harnessing AI to provide insightful responses by accessing and interpreting information from the internet, enhancing your interactive experience.")

with st.sidebar:
    st.title("Configuration")
    api_key_input = st.text_input("Enter your Gemini API Key (if available)", type="password", placeholder="If you have!")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.8, 0.1)
    model_selection = st.selectbox("Select Model", ("gemini-1.5", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-1.5-flash"))

    st.markdown("App built by Subhayu Dutta")
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_query := st.chat_input("You:"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

# Handle bot responses
if st.session_state.messages[-1]["role"] == "user":
    try:
        # Perform DuckDuckGo search
        search_response = search.run(user_query)
        print(search_response)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Given the a dictionary which contains the information 
    based on the user search query={user_query}.

    The dictionary data is:
    {search_response}

    You take all the snippet text from the dictionary and summarize them to give
    all bullet points about the query given by the users and then after that 
    provide the links as sources in bullet points. Thank you!"""
        response = model.generate_content(prompt)
        print(response)
        #bot_response = "\n".join(response.text)
        st.chat_message("assistant").write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": "Error"})
