import streamlit as st
import requests

# Backend API URL
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.set_page_config(
    page_title="AI Return Verification",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🛡️ AI-Powered Return Verification System")

# Input for Product ID
product_id = st.text_input("🔍 Enter Product ID")

# Image uploader for the return image
uploaded_file = st.file_uploader("📤 Upload Return Image", type=["jpg", "png"])

if uploaded_file and product_id:
    if st.button("✅ Verify Return"):
        try:
            # Prepare image and product ID for verification
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            # Send request to the verification endpoint
            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            if response.status_code == 200:
                result = response.json()

                # Display verification status and similarity score
                similarity_percentage = round(result['best_similarity'] * 100, 2)
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # Display the uploaded return image
                st.image(uploaded_file, caption="📷 Uploaded Return Image", use_column_width=True)

                # Fetch and display the original product images
                image_response = requests.get(f"{API_URL}/list_product_images")

                if image_response.status_code == 200:
                    images = image_response.json().get("available_images", [])

                    # Filter product images for entered product_id
                    product_images = [img for img in images if img.startswith(f"{product_id}_")]

                    if product_images:
                        st.subheader("📸 Original Product Images")
                        for img in product_images:
                            image_url = f"{API_URL}/get_product_image?filename={img}"
                            st.image(image_url, caption=f"Original: {img}", use_column_width=True)
                    else:
                        st.warning("⚠️ No original product images found for this Product ID.")
                else:
                    st.error("❌ Failed to fetch original product images.")

                # Display the stored return image (if available)
                return_image_url = f"{API_URL}/get_return_image?product_id={product_id}"
                st.subheader("📦 Stored Return Image")
                st.image(return_image_url, caption="Stored Return Image", use_column_width=True)

            else:
                st.error(f"❌ Error verifying return: {response.json().get('detail', 'Unknown error')}")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")

else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
