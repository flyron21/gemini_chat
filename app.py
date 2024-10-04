from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API for Gemini
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app configurations and style adjustments
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for enhancing the UI
st.markdown("""
    <style>
        .main {
            background-color: #1E1E1E; /* Dark grey background */
            padding: 10px;
            border-radius: 10px;
        }
        h1, h2, h3, h4 {
            color: #FFC700; /* EY yellow */
        }
        .chat-input {
            background-color: #ffffff; /* White for input box */
            border-radius: 15px;
            padding: 10px;
            width: 100%;
            color: #FFC700; /* Yellow text in input box */
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        }
        .response-container {
            background-color: #ffffff; /* White background for responses */
            color: #000000; /* Yellow text for responses */
            border-radius: 10px;
            padding: 10px;
            margin-top: 20px; /* Added margin to create space */
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        .chat-container {
            background-color: #000000; /* Black for chat messages */
            color: #FFC700; /* Yellow text on black background */
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        .chat-history-container {
            max-height: 200px; /* Limit the height of the chat history */
            overflow-y: auto; /* Enable scrolling if content overflows */
            margin-top: 30px; /* Create space between response and history */
            background-color: #333333; /* Darker background for chat history */
            border-radius: 10px;
            padding: 10px;
        }
       .send-btn {
            background-color: #FFC700; /* EY yellow */
            color: black; /* Black text for contrast */
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
            transition: background-color 0.3s ease; /* Smooth transition */
        }
        .send-btn:hover {
            background-color: #FFC700; /* Yellow on hover */
        }
    </style>
""", unsafe_allow_html=True)

# Header with custom color
st.markdown("<h1 style='text-align: center;'>Gemini Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Create a form for the chat input and button to allow "Enter" to submit
with st.form(key='chat_form'):
    # Input box with a placeholder
    input_text = st.text_input("Ask me anything:", 
                               placeholder="Type your question here...", 
                               help="Ask the Gemini chatbot anything!", 
                               max_chars=1000, 
                               key="chat_input")

    # Custom 'Ask the Question' button inside the form
    submit_button = st.form_submit_button(label="Ask the Question")

# If the form is submitted (button clicked or "Enter" pressed)
if submit_button and input_text:
    # Get the response from the Gemini API
    response = get_gemini_response(input_text)
    
    # Update the session history with user input and bot response
    st.session_state['chat_history'].append(("You", input_text))
    
    st.subheader("Response:")
    response_text = ""
    for chunk in response:
        response_text += chunk.text + " "  # Concatenate the response text
    st.markdown(f"<div class='response-container'>{response_text}</div>", unsafe_allow_html=True)
    st.session_state['chat_history'].append(("Bot", response_text))

# Chat history display with smaller size and scroll
st.subheader("Chat History")
st.markdown("<div class='chat-history-container'>", unsafe_allow_html=True)
for role, text in st.session_state['chat_history']:
    st.markdown(f"<div class='chat-container'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
