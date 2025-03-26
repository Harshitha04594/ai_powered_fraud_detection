import streamlit as st
import requests

# Backend API URL
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("🛡️ AI-Powered Return Verification System")

# Input fields
product_id = st.text_input("🔍 Enter Product ID")
uploaded_file = st.file_uploader("📤 Upload Return Image", type=["jpg", "png"])

if uploaded_file and product_id:
    if st.button("✅ Verify Return"):
        try:
            # ✅ Send return image and product ID to backend for verification
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            # Send verification request
            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            if response.status_code == 200:
                result = response.json()

                # ✅ Convert similarity score to a 1-100 scale
                similarity_percentage = round(result['best_similarity'] * 100, 2)

                # Display result
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # ✅ Show uploaded return image
                st.image(uploaded_file, caption="📷 Uploaded Return Image", use_column_width=True)

                # ✅ Fetch and display original product images
                image_response = requests.get(f"{API_URL}/list_product_images")

                if image_response.status_code == 200:
                    images = image_response.json().get("available_images", [])

                    # 🔍 Log available images for debugging
                    st.write("🔍 Available Images:", images)

                    # Filter and display images matching product_id
                    product_images = [img for img in images if img.startswith(f"{product_id}_")]

                    # 🔍 Log matched images
                    st.write("✅ Matched Images:", product_images)

                    if product_images:
                        st.subheader("📸 Original Product Images")
                        for img in product_images:
                            image_url = f"{API_URL}/get_product_image?filename={img}"
                            st.image(image_url, caption=f"Original: {img}", use_column_width=True)
                    else:
                        st.warning("⚠️ No original product images found for this Product ID.")

                else:
                    st.error("❌ Failed to fetch original product images.")

                # ✅ Display stored return image (if available)
                return_image_url = f"{API_URL}/get_return_image?product_id={product_id}"
                st.image(return_image_url, caption="📦 Stored Return Image", use_column_width=True)

            else:
                st.error("❌ Error verifying return. Check the Product ID and try again.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")

else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
