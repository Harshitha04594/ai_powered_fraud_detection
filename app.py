import streamlit as st
import requests

# ✅ FastAPI endpoint (your Render URL)
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("AI-Powered Return Verification")

# ✅ User Input: Product ID
product_id = st.text_input("Enter Product ID")

# ✅ Upload Return Image
uploaded_file = st.file_uploader("Upload Return Image", type=["jpg", "png"])

if uploaded_file and product_id:
    if st.button("Verify Return"):
        try:
            # Prepare the image and product_id
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            # Send to FastAPI endpoint
            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            # Handle the response
            if response.status_code == 200:
                result = response.json()
                similarity_percentage = result['best_similarity'] * 100
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # Display the original product images and return image
                product_images_response = requests.get(f"{API_URL}/list_product_images", params={"product_id": product_id})
                if product_images_response.status_code == 200:
                    product_images = product_images_response.json().get("available_images", [])
                    st.subheader("Original Product Images:")
                    for img_url in product_images:
                        st.image(f"{API_URL}/get_image?image_name={img_url}", caption=img_url)

                st.subheader("Returned Image:")
                st.image(uploaded_file, caption="Returned Image")

            else:
                st.error("❌ Error verifying return. Please check the Product ID and try again.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
