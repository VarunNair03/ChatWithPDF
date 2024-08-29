import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import base64
from streamlit import session_state as ss
from dotenv import load_dotenv
load_dotenv()

st.title("Chatbot")

if "messages" not in ss:
    ss.messages = []

def save_pdf():
    if ss.file:
        open("file.pdf", "wb").write(ss.file.getvalue())

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

file = st.file_uploader("Upload a PDF file", type=["pdf"], on_change=save_pdf, key="file", accept_multiple_files=False)


def call_gemini(prompt):
    gemini = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",

        )

    gemini_response = gemini.invoke(prompt)
    return gemini_response.content


    


for message in ss.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if file:
    displayPDF("file.pdf")

if prompt := st.chat_input("What is up?", key="prompt"):
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