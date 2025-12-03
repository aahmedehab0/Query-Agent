import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS - Professional Dark Theme
st.markdown("""
<style>
    /* Main background - Deep professional gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Chat messages - Enhanced glassmorphism */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        backdrop-filter: blur(20px);
        margin: 16px 0;
        padding: 8px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stChatMessageContent"] {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 500;
        line-height: 1.8;
        letter-spacing: 0.3px;
    }
    
    /* Info boxes - SQL */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 16px;
        color: #6ee7b7 !important;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    /* Info boxes - RAG */
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.1) 100%);
        border-left: 5px solid #3b82f6;
        border-radius: 12px;
        padding: 16px;
        color: #93c5fd !important;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    /* Title - Bold and prominent */
    h1 {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 42px !important;
        text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
        letter-spacing: 1px;
    }
    
    /* Selectbox - Modern styling */
    .stSelectbox label {
        color: #e0e7ff !important;
        font-weight: 600;
        font-size: 16px;
    }
    
    .stSelectbox > div > div {
        background: rgba(139, 92, 246, 0.2) !important;
        border: 2px solid rgba(139, 92, 246, 0.4) !important;
        border-radius: 12px;
        color: white !important;
        font-weight: 500;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Selectbox dropdown */
    [data-baseweb="popover"] {
        background: rgba(30, 27, 75, 0.98) !important;
        border: 2px solid rgba(139, 92, 246, 0.4) !important;
        border-radius: 12px !important;
    }
    
    /* Input field container - Remove white frame */
    .stChatInput {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 20px !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        padding: 20px !important;
        z-index: 997 !important;
    }
    
    /* Input field - Professional with glow - FIXED HEIGHT */
    .stChatInput textarea {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.95) 0%, rgba(45, 40, 90, 0.95) 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 16px;
        font-size: 17px !important;
        font-weight: 500;
        padding: 16px !important;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15);
        letter-spacing: 0.3px;
        height: 120px !important;
        min-height: 120px !important;
        max-height: 120px !important;
        resize: none !important;
        overflow-y: auto !important;
    }
    
    .stChatInput textarea::placeholder {
        color: rgba(196, 181, 253, 0.5) !important;
        font-weight: 400;
    }
    
    .stChatInput textarea:focus {
        border: 2px solid rgba(139, 92, 246, 0.9) !important;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.4);
        background: linear-gradient(135deg, rgba(30, 27, 75, 1) 0%, rgba(45, 40, 90, 1) 100%) !important;
        height: 120px !important;
    }
    
    /* Hide input field bottom toolbar */
    .stChatInput > div {
        background: transparent !important;
        border: none !important;
    }
    
    /* Caption text - Clear and visible */
    .stCaptionContainer, [data-testid="stCaptionContainer"] {
        color: rgba(196, 181, 253, 0.7) !important;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    
    /* Error messages */
    .stAlert {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
        color: #fca5a5 !important;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        font-weight: 600;
    }
    
    /* Divider line */
    hr {
        border-color: rgba(139, 92, 246, 0.2) !important;
        margin: 24px 0;
    }
    
    /* Avatar icons enhancement */
    [data-testid="chatAvatarIcon"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Bottom area - Remove white background */
    .stBottom {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Remove bottom white strip completely */
    [data-testid="stBottom"] {
        background: transparent !important;
        border: none !important;
    }
    
    /* Main container bottom fix */
    .main .block-container {
        padding-bottom: 180px !important;
        padding-top: 120px !important;
    }
    
    /* Header - Make it sticky */
    .stApp > header {
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%) !important;
        padding: 20px 0 !important;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Make title and language selector sticky */
    .main > div:first-child {
        position: sticky !important;
        top: 0 !important;
        z-index: 998 !important;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%) !important;
        padding: 20px 0 10px 0 !important;
        margin-bottom: 10px !important;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2) !important;
    }


</style>
""", unsafe_allow_html=True)

# Header with language selector
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🤖 AI Agent")
with col2:
    language = st.selectbox(
        "Input Language",
        ["Arabic", "English"],
        label_visibility="visible"
    )

st.markdown("---")

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm an AI Agent. I can help you search documents or query databases.",
        "timestamp": datetime.now().strftime("%H:%M")
    }]

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(f" {message['timestamp']}")
        
        # Show type if exists
        if "type" in message:
            if message["type"] == "SQL":
                st.success(f" {message['type']}")
            elif message["type"] == "RAG":
                st.info(f" {message['type']}")

# Handle input
if prompt := st.chat_input("Type your question here..."):
    
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f" {timestamp}")
    
    # Process response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare language code
                lang_code = "ar" if language == "Arabic" else "en"
                
                # Call LangGraph
                result = app.invoke({
                    "question": prompt,
                    "language": lang_code,
                    "use_dspy": True
                })
                
                # Extract data
                response = result.get("output_text", "Sorry, couldn't get an answer.")
                agent_type = result.get("route", "UNKNOWN").upper()
                
                # Show type
                if agent_type == "RAG":
                    st.info(f" {agent_type}")
                elif agent_type == "SQL":
                    st.success(f" {agent_type}")
                
                # Display answer
                st.markdown(response)
                st.caption(f" {timestamp}")
                
                # Save message with type
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": timestamp,
                    "type": agent_type
                })
                
            except Exception as e:
                st.error(f" Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f" Error: {str(e)}",
                    "timestamp": timestamp
                }) 