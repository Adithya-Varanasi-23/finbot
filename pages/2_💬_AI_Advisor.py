import streamlit as st
import os, sys

# Need to append parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_helper import generate_chat_response

st.set_page_config(page_title="FinAI Chatbot", page_icon="💬", layout="wide")

# Read CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💬 FinAI Advisor Chat")
st.markdown("Ask me anything about budgeting, saving, investments, taxes, EMI, or financial planning.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an initial greeting from the AI
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am your AI Financial Advisor. How can I help you manage your money today?"
    })

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., How should I split my salary?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            # Call Gemini
            response = generate_chat_response(st.session_state.messages)
            
        message_placeholder.markdown(response, unsafe_allow_html=True)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar options to clear chat
if st.sidebar.button("Clear Chat History", type="primary"):
    st.session_state.messages = []
    st.rerun()
