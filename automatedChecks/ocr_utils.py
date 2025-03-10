import cv2
import pytesseract
import os
import re
from pdf2image import convert_from_path

POPPLER_PATH = "/opt/homebrew/bin"  # Update for your system
OUTPUT_DIR = "output_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_extracted_text(text, filename):
    """Save extracted text to a file."""
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w") as file:
        file.write(text)

def process_file(file_path):
    """Process an image or PDF and return extracted text."""
    extracted_text = process_pdf(file_path) if file_path.lower().endswith('.pdf') else process_image(file_path)
    
    # Save text to file
    save_extracted_text(extracted_text, "extracted_text.txt")
    
    return extracted_text

def process_pdf(pdf_path):
    """Convert PDF pages to images and extract text."""
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    full_text = ""
    for i, img in enumerate(images):
        img_path = os.path.join("uploads", f'page_{i}.png')
        img.save(img_path, 'PNG')
        full_text += process_image(img_path) + "\n"
    
    return full_text

def process_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Unable to read the image."

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    extracted_text = pytesseract.image_to_string(otsu)
    
    return extracted_text

def process_image_adaptive(image_path):
    """Extract text from an image using Tesseract OCR with improved preprocessing."""
    image = cv2.imread(image_path)
    
    if image is None:
        return "Error: Unable to read the image."
    
    # Convert to grayscale and apply Gaussian blur to reduce noise
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding for better handling of shadows
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255,
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY,
                                           11, 2)
    
    # Find and enhance edges (for text extraction)
    edges = cv2.Canny(adaptive_thresh, 75, 150)
    
    return pytesseract.image_to_string(edges, lang='eng', config='--oem 3')

def extract_license_number(text):
    """Extract everything after 'Licence No'."""
    match = re.search(r'Licence No[:\s\._-]*(.*)', text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_registration_number(text):
    """Extract everything after 'Registration No'."""
    match = re.search(r'CEA Registration No[:\s\._-]*(.*)', text, re.IGNORECASE)
    return match.group(1).strip() if match else None
