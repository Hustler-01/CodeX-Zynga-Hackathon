import easyocr
import re
from datetime import datetime
import torch
from pdf2image import convert_from_path
import os

def convert_pdf_to_image(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        if not images:
            raise ValueError("No images generated from PDF")
        img_path = pdf_path.replace('.pdf', '.jpg')
        images[0].save(img_path, 'JPEG')
        return img_path
    except Exception as e:
        print(f"❌ PDF conversion failed: {e}")
        raise

def compute_age(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except Exception as e:
        print(f"❌ DOB parsing failed: {e}")
        return 0

def ocr_extract_info(image_path):
    # Handle PDF if needed
    if image_path.lower().endswith(".pdf"):
        image_path = convert_pdf_to_image(image_path)

    aadhaar_langs = ['en', 'hi']  # Use only supported languages

    gpu_available = torch.cuda.is_available()
    print(f"👉 EasyOCR — using GPU: {gpu_available}")

    try:
        reader = easyocr.Reader(aadhaar_langs, gpu=gpu_available)
    except Exception as e:
        print(f"❌ EasyOCR Reader initialization failed: {e}")
        raise

    try:
        result = reader.readtext(image_path, detail=0)
        full_text = " ".join(result)
        print(f"[EasyOCR] Full text: {full_text}")
    except Exception as e:
        print(f"❌ OCR reading failed: {e}")
        return {
            'dob': 'N/A',
            'age': 0,
            'is_18_or_more': False
        }

    # Extract DOB
    dob_match = re.search(r'\d{2}/\d{2}/\d{4}', full_text)
    if dob_match:
        dob = dob_match.group(0)
    else:
        dob = "DOB not found"

    age_years = compute_age(dob) if dob != "DOB not found" else 0
    is_18_plus = bool(age_years >= 18)  # ✅ Ensure native Python bool

    return {
        'dob': dob,
        'age': int(age_years),           # ✅ Ensure native int
        'is_18_or_more': is_18_plus
    }

