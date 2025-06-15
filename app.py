import streamlit as st
import google.generativeai as genai
from PIL import Image

# Gemini setup
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# App config
st.set_page_config(page_title="Accessibility Caption Generator")
st.title("Accessibility Caption Generator")
st.write("Upload an image to generate a concise accessibility-friendly caption.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Analyzing image..."):
            response = model.generate_content(
                [uploaded_file.getvalue()],
                mime_type="image/png",
                prompt="Generate a short, descriptive alt text caption for this image suitable for screen readers."
            )
            caption = response.text.strip()

            st.subheader("Generated Caption")
            st.success(caption)
