import streamlit as st
from PIL import Image
from google import genai

# Load API Key from Streamlit secrets
api_key = st.secrets["api_keys"]["google_api_key"]
client = genai.Client(api_key=api_key)

# Set up Streamlit UI
st.set_page_config(page_title="Accessibility Caption Generator")
st.title("Accessibility Caption Generator")
st.write("Upload an image to generate an accessibility-friendly caption for screen readers.")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            # Load image bytes
            image_bytes = uploaded_file.read()

            # Generate caption using Gemini
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[
                    {"role": "user", "parts": [
                        {"inline_data": {"mime_type": "image/png", "data": image_bytes}},
                        {"text": "Generate a short and clear alt text description for this image, suitable for accessibility purposes."}
                    ]}
                ]
            )

            st.subheader("Generated Caption")
            st.success(response.text.strip())
