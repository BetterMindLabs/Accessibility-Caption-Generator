import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure Gemini
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="Accessibility Caption Generator")
st.title("Accessibility Caption Generator")
st.write("Upload an image to generate an alt text caption for screen reader accessibility.")

# File upload
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Analyzing image..."):
            image_bytes = uploaded_file.read()

            # Send image + instruction to Gemini
            response = model.generate_content([
                genai.types.ContentPart.from_image_data(image_bytes),
                genai.types.ContentPart.from_text("Generate a concise, accessibility-friendly alt text caption for this image.")
            ])

            caption = response.text.strip()
            st.subheader("Generated Caption")
            st.success(caption)
