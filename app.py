import streamlit as st
import requests

# ✅ Update the FastAPI endpoint
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("AI-Powered Return Verification")

uploaded_file = st.file_uploader("Upload return image", type=["jpg", "png"])

if uploaded_file:
    product_id = st.text_input("Enter Product ID")
    if st.button("Verify Return"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/verify_return", files=files, params={"product_id": product_id})
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Status: {result['status']}")
            st.info(f"Similarity: {result['best_similarity']:.2f}")
        else:
            st.error("Error verifying return. Check the product ID or try again.")
