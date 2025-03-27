import streamlit as st
import requests

# Backend API URL
API_URL = "https://ai-powered-fraud-detection.onrender.com"

# Custom CSS for Light Blue Background & White Content Box
st.markdown(
    """
    <style>
        /* Light Blue Background */
        .stApp {
            background-color: #ADD8E6;  /* Light Blue */
        }

        /* White Centered Content Box */
        .content-container {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.3);
            margin: auto;
            width: 80%;
            text-align: center;
        }

        /* Marquee Effect */
        .marquee-container {
            background: linear-gradient(to right, #1E90FF, #00BFFF);  /* Darker Blue Gradient */
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            overflow: hidden;
        }

        .marquee {
            display: inline-block;
            white-space: nowrap;
            animation: marquee 10s linear infinite;
        }

        @keyframes marquee {
            from { transform: translateX(100%); }
            to { transform: translateX(-100%); }
        }

    </style>

    <!-- Marquee Banner -->
    <div class="marquee-container">
        <span class="marquee">🚀 AI-Powered Return Verification System - Secure & Smart! 🛡️</span>
    </div>
    """,
    unsafe_allow_html=True
)

# White Content Box
st.markdown('<div class="content-container">', unsafe_allow_html=True)
st.title("🛡️ AI-Powered Return Verification System")

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
                st.success(f"✅ Status: {result['status']}")
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

st.markdown('</div>', unsafe_allow_html=True)  # Close the content box
