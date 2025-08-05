import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/predict"  # Change to Render/Deployment URL when needed

st.title("♻️ Smart Waste Classifier")

# User selection
input_option = st.radio("Choose Image Input Method", ["📁 Upload Image", "📸 Use Camera"])

image_bytes = None

# Option 1: File uploader
if input_option == "📁 Upload Image":
    uploaded_file = st.file_uploader("Upload an image of waste", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image_bytes = uploaded_file.read()
        st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

# Option 2: Camera input
elif input_option == "📸 Use Camera":
    camera_file = st.camera_input("Take a picture")
    if camera_file:
        image_bytes = camera_file.getvalue()
        st.image(image_bytes, caption="Captured Image", use_column_width=True)

# Prediction
if image_bytes is not None:
    with st.spinner("Classifying the image..."):
        files = {"file": image_bytes}
        try:
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                result = response.json()
                predicted_class = result.get("class", "Unknown")
                st.success(f"✅ Predicted Waste Category: **{predicted_class}**")

                # Tips for each class
                tips = {
                    "N": "🗑️ **Non-Recyclable** – Dispose responsibly, do not mix with recyclables.",
                    "O": "🌱 **Organic** – Compost it! Great for your garden or community compost.",
                    "R": "♻️ **Recyclable** – Rinse and recycle in your designated bin.",
                }
                st.info(tips.get(predicted_class, "No tips available for this category."))
            else:
                st.error("Prediction failed. Check FastAPI server.")
        except Exception as e:
            st.error(f"Error: {e}")
