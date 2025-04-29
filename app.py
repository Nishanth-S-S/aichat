import streamlit as st
import google.generativeai as genai

# ---- API Key ----
GOOGLE_API_KEY = "AIzaSyAZA2aZfWN-P6-3w6Oq7QOMGh99bxswD3o"
genai.configure(api_key=GOOGLE_API_KEY)

# ---- Initialize Gemini Model ----
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")  # <-- correct model name now!

# ---- Streamlit UI ----
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Chat with Gemini 1.5 Pro")

# ---- Initialize chat history ----
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---- Display chat messages from history ----
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# ---- User input ----
prompt = st.chat_input("Say something...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send user input to Gemini
    response = st.session_state.chat.send_message(prompt)

    # Display Gemini response
    with st.chat_message("assistant"):
        st.markdown(response.text)
