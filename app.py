import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="Accessibility Caption Generator")
st.title("Accessibility Caption Generator")
st.write("Upload an image to generate a concise alt text caption for screen readers and accessibility tools.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Analyzing image..."):
            image_bytes = uploaded_file.getvalue()
            response = model.generate_content([
                {"mime_type": "image/png", "data": image_bytes},
                {"text": "Generate a short, descriptive alt text caption for this image suitable for screen readers."}
            ])
            caption = response.text.strip()

            st.subheader("Generated Caption")
            st.success(caption)
