import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Set Streamlit page config
st.set_page_config(page_title="Gemini 1.5 Pro Chat", page_icon="🤖", layout="centered")

st.title("🤖 Gemini 1.5 Pro Chat with Image Support")

# API Key input (store securely in session state)
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input("Enter your Google Gemini API Key", type="password", value=st.session_state.api_key)
if api_key:
    st.session_state.api_key = api_key

if not api_key:
    st.warning("Please enter your Google Gemini API key to continue.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create Gemini 1.5 Pro chat model
@st.cache_resource
def get_chat_model():
    return genai.GenerativeModel("gemini-1.5-pro")

model = get_chat_model()

# Image uploader
uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

# User input
user_message = st.text_input("Your message:", key="user_message")

# Send button
if st.button("Send", use_container_width=True):
    if not user_message and not uploaded_image:
        st.warning("Please enter a message or upload an image.")
    else:
        # Prepare content parts
        content = []
        if user_message:
            content.append(user_message)
        if uploaded_image:
            image = Image.open(uploaded_image)
            # Convert image to bytes for Gemini SDK
            img_bytes = io.BytesIO()
            image.save(img_bytes, format=image.format if image.format else "PNG")
            img_bytes.seek(0)
            content.append(
                genai.types.content_types.Part(
                    inline_data=genai.types.content_types.Blob(
                        mime_type=uploaded_image.type,
                        data=img_bytes.read()
                    )
                )
            )

        # Add user message to chat history
        st.session_state.chat_history.append(("user", user_message, uploaded_image))

        # Send to Gemini
        try:
            response = model.generate_content(content)
            gemini_reply = response.text
        except Exception as e:
            gemini_reply = f"Error: {e}"

        # Add Gemini reply to chat history
        st.session_state.chat_history.append(("gemini", gemini_reply, None))

# Display chat history
for sender, message, img in st.session_state.chat_history:
    if sender == "user":
        st.markdown("**You:**")
        if message:
            st.markdown(message)
        if img:
            st.image(img, width=200)
    else:
        st.markdown("**Gemini:**")
        st.markdown(message)

st.markdown("---")
st.caption("Built with Streamlit & Google Gemini 1.5 Pro")

