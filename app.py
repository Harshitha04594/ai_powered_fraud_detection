import streamlit as st
import requests

# ✅ FastAPI endpoint (your Render URL)
API_URL = "https://ai-powered-fraud-detection.onrender.com"

st.title("AI-Powered Return Verification")

# ✅ User Input: Product ID
product_id = st.text_input("Enter Product ID")

# ✅ Upload Return Image
uploaded_file = st.file_uploader("Upload Return Image", type=["jpg", "png"])

# ✅ Fetch and display original product images
if product_id:
    try:
        response = requests.get(f"{API_URL}/list_product_images")
        if response.status_code == 200:
            images = response.json().get("available_images", [])
            product_images = [img for img in images if img.startswith(f"{product_id}_")]

            if product_images:
                st.subheader("📸 Original Product Images:")
                for img_name in product_images:
                    img_url = f"{API_URL}/static/{img_name}"
                    st.image(img_url, caption=img_name, width=300)
            else:
                st.warning(f"No images found for Product ID: {product_id}")
        else:
            st.error("❌ Failed to fetch product images.")
    except Exception as e:
        st.error(f"⚠️ Error fetching images: {e}")

# ✅ Verify the return image
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
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {result['best_similarity']:.2f}")
            else:
                st.error("❌ Error verifying return. Please check the Product ID and try again.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
