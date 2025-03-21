import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from typing import List
import logging

app = FastAPI()

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)

# ✅ Directories for image storage (Linux-compatible paths for Render)
BASE_DIR = "/opt/render/project/src"
PRODUCT_IMAGES_DIR = os.path.join(BASE_DIR, "product_images")
RETURNED_IMAGES_DIR = os.path.join(BASE_DIR, "returned_images")

# ✅ Ensure directories exist
os.makedirs(PRODUCT_IMAGES_DIR, exist_ok=True)
os.makedirs(RETURNED_IMAGES_DIR, exist_ok=True)

# ✅ Debug message to confirm the file is running
logging.info("✅ FastAPI is running the updated mini_projects.py")

# ✅ Function to compute Structural Similarity Index (SSIM)
def compare_images(img1_path, img2_path):
    logging.info(f"🔍 Comparing images: {img1_path} vs {img2_path}")
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        logging.error(f"❌ Image loading failed: {img1_path} or {img2_path}")
        return 0.0  # Return 0.0 if images cannot be loaded

    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))

    score, _ = ssim(img1, img2, full=True)
    return score

# ✅ Helper function to fetch stored images by product_id
def get_product_images(product_id):
    try:
        if not os.path.exists(PRODUCT_IMAGES_DIR):
            logging.error("❌ Product images directory does not exist!")
            return []
        
        product_images = [f for f in os.listdir(PRODUCT_IMAGES_DIR) if f.startswith(f"{product_id}_")]
        logging.info(f"📸 Found images for {product_id}: {product_images}")
        return product_images

    except Exception as e:
        logging.error(f"❌ Error fetching product images: {e}")
        return []

# ✅ Endpoint: Upload multiple images for a product
@app.post("/upload_product_images")
async def upload_product_images(product_id: str, files: List[UploadFile] = File(...)):
    try:
        logging.info(f"📤 Uploading images for product_id: {product_id}")

        saved_files = []
        for idx, file in enumerate(files):
            file_path = os.path.join(PRODUCT_IMAGES
