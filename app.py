import streamlit as st
import requests

<<<<<<< HEAD
# Replace this with your Render API URL
API_URL = "https://return-verification-api-1.onrender.com"

st.title("Return Verification App")

# --- Upload Product Images ---
st.header("Upload Product Images")
product_id = st.text_input("Enter Product ID", value="prod1")
uploaded_files = st.file_uploader("Choose Product Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("Upload Images"):
    if not product_id:
        st.error("Please enter a product ID.")
    elif not uploaded_files:
        st.error("Please select at least one image file.")
    else:
        files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
        response = requests.post(f"{API_URL}/upload_product_images", params={"product_id": product_id}, files=files)
        if response.status_code == 200:
            st.success("Images uploaded successfully!")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)

# --- Verify a Return Image ---
st.header("Verify Return")
return_file = st.file_uploader("Choose Return Image", type=["jpg", "jpeg", "png"], key="return")
if st.button("Verify Return"):
    if not product_id:
        st.error("Please enter a product ID.")
    elif not return_file:
        st.error("Please select a return image.")
    else:
        files = {"file": (return_file.name, return_file.getvalue(), return_file.type)}
        response = requests.post(f"{API_URL}/verify_return", params={"product_id": product_id}, files=files)
        if response.status_code == 200:
            st.success("Return verified!")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)

# --- View All Products ---
st.header("View All Products")
if st.button("Get Products"):
    response = requests.get(f"{API_URL}/products/")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)
=======
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
                st.success(f"✅ Status: {result['status']}")
                st.info(f"📊 Similarity: {result['best_similarity']:.2f}")
            else:
                st.error("❌ Error verifying return. Please check the Product ID and try again.")
        
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("⚠️ Please enter a Product ID and upload a return image.")
>>>>>>> ec4b669f5958924a40113e926773adba197929dd
