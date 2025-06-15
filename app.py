import streamlit as st
from PIL import Image
import base64
import requests
from io import BytesIO

# ============ Gemini API Setup ============
API_KEY = st.secrets["google_api_key"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def image_to_base64(img: Image.Image):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def call_gemini_with_image(image_data_b64, prompt_text):
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_data_b64
                        }
                    },
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }
    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", headers=headers, json=body)
    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Gemini API Error."

# ============ Streamlit UI ============
st.set_page_config(page_title="Accessibility Caption Generator")
st.title("Accessibility Caption Generator")
st.write("Upload an image to generate an alt text caption for screen reader accessibility.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Analyzing image..."):
            image_b64 = image_to_base64(image)
            prompt = "Generate a short, descriptive alt text caption for this image suitable for screen readers."
            result = call_gemini_with_image(image_b64, prompt)

        st.subheader("Generated Caption")
        st.success(result)
