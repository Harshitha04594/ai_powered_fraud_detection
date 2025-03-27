import streamlit as st
import requests

# Apply custom CSS for background color
st.markdown(
    """
    <style>
        /* Background color */
        body {
            background-color: #f0f2f6;  /* Light Gray */
        }
        /* Customizing Titles */
        .stApp {
            background-color: #e6f7ff;  /* Light Blue */
        }
        h1 {
            color: #007BFF;  /* Blue */
            font-size: 32px;
        }
        h2, h3 {
            color: #003366;  /* Dark Blue */
        }
        /* Buttons */
        .stButton>button {
            background-color: #007BFF;
            color: white;
            font-size: 16px;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ AI-Powered Return Verification System")

# Backend API URL
API_URL = "https://ai-powered-fraud-detection.onrender.com"

# Input fields
product_id = st.text_input("🔍 Enter Product ID")
uploaded_file = st.file_uploader("📤 Upload Return Image", type=["jpg", "png"])

if uploaded_file and product_id:
    if st.button("✅ Verify Return"):
        try:
            # ✅ Send return image and product ID for verification
            files = {"file": uploaded_file.getvalue()}
            params = {"product_id": product_id}

            # Send verification request
            response = requests.post(f"{API_URL}/verify_return", files=files, params=params)

            if response.status_code == 200:
                result = response.json()

                # ✅ Convert similarity score to 1-100 scale
                similarity_percentage = round(result['best_similarity'] * 100, 2)

                # Display verification results
                if result['status'] == "Approved":
                    st.success(f"✅ Status: {result['status']}")
                else:
                    st.error(f"❌ Status: {result['status']}")

                st.info(f"📊 Similarity: {similarity_percentage:.2f}%")

                # ✅ Show uploaded return image
                st.image(uploaded_file, caption="📷 Uploaded Return Image", use_column_width=True)

                # ✅ Fetch and display original product images
                image_response = requests.get(f"{API_URL}/list_product_images")
                
                if image_response.status_code == 200:
                    images = image_response.json().get("available_images", [])
                    st.write("📂 Available Images from Backend:", images)  # Debugging output

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
