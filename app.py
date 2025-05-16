

import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ---- CONFIG ----
genai.configure(api_key="AIzaSyAZA2aZfWN-P6-3w6Oq7QOMGh99bxswD3o")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to 1.5 flash

st.set_page_config(page_title="Gemini Chat with Image", layout="wide")
st.title("Gemini 1.5 Flash Chatbot (Text + Image)")

# ---- SESSION STATE ----
if "history" not in st.session_state:
    st.session_state.history = []

# ---- INPUT AREA ----
with st.sidebar:
    st.subheader("Input")
    user_input = st.text_area("Enter your message", height=150)
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
    send_btn = st.button("Send")

# ---- HANDLE SEND ----
if send_btn and (user_input or uploaded_image):
    content = []

    if uploaded_image:
        image_bytes = uploaded_image.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        content.append(image)

    if user_input:
        content.append(user_input)

    try:
        response = model.generate_content(content)
        reply = response.text

        st.session_state.history.append({
            "user": user_input,
            "image": uploaded_image,
            "bot": reply
        })
    except Exception as e:
        st.error(f"Error: {e}")

# ---- DISPLAY CHAT ----
st.subheader("Conversation")
for chat in st.session_state.history[::-1]:
    with st.container():
        st.markdown(f"**You:** {chat['user']}")
        if chat["image"]:
            st.image(chat["image"], width=300)
        st.markdown(f"**Gemini:** {chat['bot']}")
        st.markdown("---")
