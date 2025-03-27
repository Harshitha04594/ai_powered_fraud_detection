import streamlit as st
import requests
from PIL import Image
import io

# Set Page Config
st.set_page_config(page_title="AI-Powered Return Verification", page_icon="🛡️", layout="wide")

# Apply Custom CSS for Styling
st.markdown(
    """
    <style>
        /* Background Styling */
        body {
            background-color: white;
        }

        .stApp {
            background-color: white;
        }

        /* Centered Content Box */
        .main-container {
            background-color: #b0d4f1;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            margin: auto;
        }

        /* Marquee Styling */
        .marquee-container {
            background: linear-gradient(to right, #008CBA, #005F7F);
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        /* Custom Button */
        .stButton>button {
            background-color: #008CBA;
            color: white;
            padding: 8px 15px;
            border-radius: 8px;
            font-weight: bold;
        }

        /* Input Field Styling */
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# Marquee Message
st.markdown('<div class="marquee-container">🚀 AI-Powered Return Verification System - Secure & Smart! 🚀</div>', unsafe_allow_html=True)

# Centered Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.markdown("### 🛡️ AI-Powered Return Verification System", unsafe_allow_html=True)

# Input: Product ID
product_id = st.text_input("🔍 Enter Product ID")

# Upload Image
uploaded_file = st.file_uploader("📤 Upload Return Image", type=["jpg", "jpeg", "png"])

# Verify Button
if st.button("✅ Verify Return"):
    if uploaded_file and product_id:
        # Convert uploaded file to bytes
        img_bytes = uploaded_file.read()

        # Send request to FastAPI for verification
        files = {"file": (uploaded_file.name, img_bytes, "image/jpeg")}
        response = requests.post(f"http://127.0.0.1:8000/verify_return?product_id={product_id}", files=files)

        if response.status_code == 200:
            result = response.json()
            similarity = result["best_similarity"] * 100
            status = result["status"]

            # Display Result
            st.success(f"✅ Status: {status}")
            st.info(f"📊 Similarity: {similarity:.2f}%")
        else:
            st.error("❌ Error processing the request.")
    else:
        st.warning("⚠️ Please enter a Product ID and upload an image.")

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
