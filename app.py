import streamlit as st
import requests

API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("AI-Powered Return Verification System")

product_id = st.text_input("Enter Product ID")
uploaded_file = st.file_uploader("Upload Return Image", type=["jpg", "png"])

if uploaded_file and product_id:
    if st.button("Verify Return"):
        try:
            # ✅ Send request to verify the return image
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            if response.status_code == 200:
                result = response.json()
                
                # ✅ Convert similarity score to 1-100 scale
                similarity_percentage = round(result['best_similarity'] * 100, 2)

                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # ✅ Show uploaded return image
                st.image(uploaded_file, caption="Uploaded Return Image", use_column_width=True)

                # ✅ Fetch and display original product images
                image_response = requests.get(f"{API_URL}/list_product_images")
                if image_response.status_code == 200:
                    images = image_response.json().get("available_images", [])
                    product_images = [img for img in images if img.startswith(f"{product_id}_")]
                    for img in product_images:
                        st.image(f"{API_URL}/get_product_image?filename={img}", caption=f"Original: {img}", use_column_width=True)

                # ✅ Display stored return image from backend
                return_image_url = f"{API_URL}/get_return_image?product_id={product_id}"
                st.image(return_image_url, caption="Stored Return Image", use_column_width=True)

            else:
                st.error("❌ Error verifying return. Check the Product ID and try again.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
