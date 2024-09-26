import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
import base64
from streamlit import session_state as ss
import os
from dotenv import load_dotenv
from embedchain import App
load_dotenv()


config = {
    "llm" : {
        "provider" : "google",
        "config" : {
            "model" : "gemini-1.5-flash",
            "max_tokens" : 10000,
            "temperature" : 0.5,

        
        }   ,
        },
        'embedder': {
        'provider': 'google',
        'config': {
        'model': 'models/text-embedding-004',
    }
  }
}



st.title("Chatbot")

save_path = "uploaded_files"
c1, c2 = st.columns([3, 1])

if "messages" not in ss:
    ss.messages = []
    os.remove("db")
def delete_files():
    all_files = os.listdir(save_path)
    for file in all_files:
        file_path = os.path.join(save_path, file)
        if os.path.isfile(file_path) and file not in ss.files:
            os.remove(file_path)
def save_pdf():
    ss.app =  App.from_config(config=config)
    os.makedirs(save_path ,exist_ok=True) 
    delete_files()
    
    if ss.files:
        for file in ss.files:
            with open(os.path.join(save_path, file.name), "wb") as f:
                f.write(file.getbuffer())

    if ss.files:
        for file in ss.files:
            file_path = os.path.join(save_path, file.name)
            print(file_path)
            if os.path.isfile(file_path):
                ss.app.add(file_path)
    if not ss.files:
        ss.files = []
        ss.messages = []

    


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

file = st.file_uploader("Upload a PDF file", type=["pdf"], on_change=save_pdf, key="files", accept_multiple_files=True)


def call_gemini(prompt):
    gemini = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        )
    
    resp = ss.app.query(prompt)
    print(resp)
    return resp


    


for message in ss.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if file:
    if prompt := st.chat_input("What do you wanna ask about the pdfs?", key="prompt"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        ss.messages.append({"role": "user", "content": prompt})

        response = call_gemini(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        ss.messages.append({"role": "assistant", "content": response})
else:
    st.write("Please upload a PDF file first")