import streamlit as st
import requests

# Backend API URL
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("🛡️ AI-Powered Return Verification System")

# ✅ Input fields
product_id = st.text_input("🔍 Enter Product ID").strip()  # Strip spaces
uploaded_file = st.file_uploader("📤 Upload Return Image", type=["jpg", "png"])

# Debugging Output (Check on Mobile)
st.write(f"📌 Debug: Entered Product ID -> `{product_id}`")  

if uploaded_file and product_id:
    if st.button("✅ Verify Return"):
        try:
            # ✅ Send return image and product ID for verification
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            # API Call for Verification
            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            if response.status_code == 200:
                result = response.json()

                # ✅ Convert similarity score to 1-100 scale
                similarity_percentage = round(result['best_similarity'] * 100, 2)

                # Display verification results
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # ✅ Show uploaded return image
                st.image(uploaded_file, caption="📷 Uploaded Return Image", use_column_width=True)

                # ✅ Fetch and display original product images
                image_response = requests.get(f"{API_URL}/list_product_images?product_id={product_id}")
                
                if image_response.status_code == 200:
                    images = image_response.json().get("available_images", [])
                    st.write(f"📂 Available Images for `{product_id}`:", images)  # Debugging output

                    if images:
                        st.subheader("📸 Original Product Images")
                        for img in images:
                            image_url = f"{API_URL}/get_product_image?filename={img}"
                            st.image(image_url, caption=f"Original: {img}", use_column_width=True)
                    else:
                        st.warning("⚠️ No original product images found for this Product ID.")

                else:
                    st.error(f"❌ Failed to fetch original product images. Error: {image_response.text}")

                # ✅ Display stored return image (if available)
                return_image_url = f"{API_URL}/get_return_image?product_id={product_id}"
                st.image(return_image_url, caption="📦 Stored Return Image", use_column_width=True)

            else:
                st.error(f"❌ Error verifying return. Response: {response.text}")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")

else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
