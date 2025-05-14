import streamlit as st
import google.generativeai as genai

# ---- API Key ----
GOOGLE_API_KEY = "AIzaSyAZA2aZfWN-P6-3w6Oq7QOMGh99bxswD3o"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# ---- Initialize Gemini Model ----
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-vision") # Use the vision model

# ---- Streamlit UI ----
st.set_page_config(page_title="Gemini Chatbot with Images", page_icon="🖼️")
st.title("🖼️ Chat with Gemini 1.5 Pro Vision")

# ---- Initialize chat history ----
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---- Display chat messages from history ----
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        for part in msg.parts:  # Handle multiple parts (text and images)
            if part.text:
                st.markdown(part.text)
            elif part.image:
                st.image(part.image.decode())  # Decode image bytes


# ---- User input (Text and Image) ----
prompt = st.chat_input("Enter text or upload an image...")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])


if prompt or uploaded_file:
    # Display user message (text and/or image)
    with st.chat_message("user"):
        if prompt:
            st.markdown(prompt)
        if uploaded_file:
            st.image(uploaded_file)


    # Send user input to Gemini
    message_parts = []
    if prompt:
        message_parts.append(genai.messages.MessagePart(text=prompt))
    if uploaded_file:
        image_bytes = uploaded_file.read()
        message_parts.append(genai.messages.MessagePart(image=image_bytes))

    response = st.session_state.chat.send_message(*message_parts) # unpack parts


    # Display Gemini response (text and/or image)
    with st.chat_message("assistant"):
        for part in response.parts:
            if part.text:
                st.markdown(part.text)
            elif part.image:
                st.image(part.image.decode())
