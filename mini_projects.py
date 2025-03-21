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

# ✅ Directories for image storage
PRODUCT_IMAGES_DIR = "C:/mini_project_data/product_images"
RETURNED_IMAGES_DIR = "returned_images/"
os.makedirs(RETURNED_IMAGES_DIR, exist_ok=True)

# ✅ Debug: Ensure this file is loaded
logging.info("✅ FastAPI is running the latest mini_projects.py")

# ✅ Function to compute Structural Similarity Index (SSIM)
def compare_images(img1_path, img2_path):
    logging.info(f"Comparing images: {img1_path} vs {img2_path}")
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    if img1 is None or img2 is None:
        logging.error(f"Image loading failed: {img1_path} or {img2_path}")
        return 0.0  # Error case if images are not loaded
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    score, _ = ssim(img1, img2, full=True)
    return score

# ✅ Helper function to auto-fetch stored images by product_id
def get_product_images(product_id):
    try:
        if not os.path.exists(PRODUCT_IMAGES_DIR):
            logging.error("❌ Product images directory does not exist!")
            return []

        product_images = [f for f in os.listdir(PRODUCT_IMAGES_DIR) if f.startswith(f"{product_id}_")]
        logging.info(f"Found images for {product_id}: {product_images}")
        return product_images

    except Exception as e:
        logging.error(f"❌ Error fetching product images: {e}")
        return []

# ✅ Verify return image by comparing with stored product images
@app.post("/verify_return")
async def verify_return(product_id: str, file: UploadFile = File(...)):
    try:
        logging.info(f"🔎 Verifying return for product_id: {product_id}")
        
        # ✅ Save the uploaded return image
        returned_path = os.path.join(RETURNED_IMAGES_DIR, f"{product_id}_returned.jpg")
        with open(returned_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Auto-fetch corresponding product images
        product_images = get_product_images(product_id)
        
        if not product_images:
            raise HTTPException(status_code=404, detail=f"No product images found for product_id: {product_id}")

        # ✅ Compare return image with stored product images
        best_similarity = 0.0
        for img in product_images:
            product_img_path = os.path.join(PRODUCT_IMAGES_DIR, img)
            similarity_score = compare_images(product_img_path, returned_path)
            best_similarity = max(best_similarity, similarity_score)

        status = "Approved" if best_similarity > 0.8 else "Rejected"

        logging.info(f"✅ Verification complete. Status: {status}, Similarity: {best_similarity}")

        return {
            "status": status,
            "best_similarity": best_similarity,
            "product_id": product_id
        }

    except Exception as e:
        logging.error(f"❌ Internal Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
