import streamlit as st
import requests

# ✅ FastAPI endpoint (your Render URL)
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("🛡️ AI-Powered Return Verification")

# ✅ User Input: Product ID
product_id = st.text_input("🔢 Enter Product ID")

# ✅ Upload Return Image
uploaded_file = st.file_uploader("📤 Upload Return Image", type=["jpg", "png"])

if uploaded_file and product_id:
    if st.button("✅ Verify Return"):
        try:
            # Prepare the image and product_id
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            # Send to FastAPI endpoint for verification
            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            # Handle the response
            if response.status_code == 200:
                result = response.json()
                similarity_percentage = result['best_similarity'] * 100

                # Display status and similarity score
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # Fetch and display the original product images
                product_images_response = requests.get(f"{API_URL}/list_product_images")
                if product_images_response.status_code == 200:
                    product_images = product_images_response.json().get("available_images", [])

                    # Filter only matching product images
                    matched_images = [img for img in product_images if img.startswith(f"{product_id}_")]

                    if matched_images:
                        st.subheader("📸 Original Product Images:")
                        for img_name in matched_images:
                            img_url = f"{API_URL}/get_image?image_name={img_name}"
                            st.image(img_url, caption=f"🗂️ {img_name}")
                    else:
                        st.warning("⚠️ No images found for the given Product ID.")

                # Display the returned image
                st.subheader("🔄 Returned Image:")
                st.image(uploaded_file, caption="Returned Image")

            else:
                st.error("❌ Error verifying return. Please check the Product ID and try again.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
