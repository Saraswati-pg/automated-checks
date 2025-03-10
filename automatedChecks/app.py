from flask import Flask, request, render_template
import os
from automatedChecks.ocr_utils import process_file, extract_license_number, extract_registration_number
from automatedChecks.api_utils import fetch_cea_profile
from automatedChecks.scrap import fetchDetails
import time

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_app():
    """Create Flask app."""
    # app = Flask(__name__.split(".")[0])
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    # Define routes
    @app.route('/')
    def index():
        return '''
        <!doctype html>
        <title>Upload an Image or PDF</title>
        <h1>Upload an Image or PDF to Extract License Number</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return "No file uploaded"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Start timing
        start_time = time.time()

        # Extract text from image or PDF
        extracted_text = process_file(file_path)

        # Measure OCR extraction time
        ocr_start = time.time()

        # Extract license number
        license_number = extract_license_number(extracted_text)
        registration_number = extract_registration_number(extracted_text)

        ocr_end = time.time()
        ocr_time = ocr_end - ocr_start

        identifier = license_number if license_number else registration_number
        if not identifier:
            return "Identifier Not Found"
        
        # Measure API call time
        api_start = time.time()
        api_response = fetch_cea_profile(identifier)
        api_end = time.time()
        api_time = api_end - api_start

        # Measure scraping time
        scrap_start = time.time()
        scrap_response = fetchDetails(identifier)
        scrap_end = time.time()
        scrap_time = scrap_end - scrap_start
        

        print(f"\nOCR Extraction Time: {ocr_time:.4f} seconds")
        print(f"API Call Time: {api_time:.4f} seconds")
        print(f"Scraping Time: {scrap_time:.4f} seconds")

        return f"Extracted Identifier: {identifier}<br>API Response: {api_response}<br>Scrap Response: {scrap_response}"  
        # return f"Extracted Identifier: {identifier}<br>API Response: {api_response}"
        # Print timing information

    return app

# Entry point for running the app
if __name__ == "__main__":
    app = create_app()  # Now app is returned by create_app
    app.run(debug=True)

