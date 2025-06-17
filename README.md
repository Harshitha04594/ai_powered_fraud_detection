# AI-Powered Return Verification System

This project is designed to help delivery agents verify the authenticity of returned products using AI and image comparison. It compares uploaded return images with original product images stored in a folder, using computer vision techniques to detect mismatches and prevent fraudulent returns.

---

# Key Features

- Delivery agent login system
- Upload interface for return product image
- Automatic product image retrieval from `product_images/` based on product ID
- Image comparison using **OpenCV** and similarity scoring
- Accept or reject return based on threshold

---

## 🧠 Tech Stack

- Python
- OpenCV
- Streamlit
- NumPy
- Local File System -for image storage

---

## 📁 Project Structure

├── app.py # Main Streamlit application
├── mini_projects.py # Helper functions and logic for image comparison
├── requirements.txt # Python dependencies
├── product_images/ # Folder containing original product images
└── README.md # Project overview and documentation

1. Install Dependencies
   pip install -r requirements.txt

2.Run the Streamlit app
   streamlit run app.py

How It Works:

Delivery agent logs in
Enters product ID and uploads the return image
System fetches the original product image from product_images
Compares both images using OpenCV and calculates similarity 

##  Sample Demo
 [Click here to watch the demo video](https://youtu.be/VdHONrstCI8?si=Rq6zmhuQcPT8rfyf)

##  Live Demo

 Try the AI-Powered Return Verification System live:  
 [Click here to access the deployed app](https://aipoweredfrauddetection.streamlit.app/)


