from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import easyocr
from PIL import Image
import io
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def process_receipt(image_bytes):
    """Process the receipt image and extract relevant information."""
    try:
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Perform OCR
        results = reader.readtext(image)
        
        # Extract text from results
        text_results = [result[1] for result in results]
        
        # TODO: Implement more sophisticated parsing logic
        # This is a basic implementation that looks for price patterns
        items = []
        for i, text in enumerate(text_results):
            # Look for price patterns ($XX.XX)
            price_match = re.search(r'\$?(\d+\.\d{2})', text)
            if price_match and i > 0:  # If we find a price and there's a previous line
                price = float(price_match.group(1))
                name = text_results[i-1]  # Assume the previous line is the item name
                items.append({
                    "name": name,
                    "price": price
                })
        
        # TODO: Extract store name and date
        # For now, using placeholder data
        return {
            "store": "Sample Store",
            "date": datetime.now().isoformat(),
            "items": items
        }
    
    except Exception as e:
        print(f"Error processing receipt: {str(e)}")
        return None

@app.route('/api/upload', methods=['POST'])
def upload_receipt():
    """Handle receipt upload and processing."""
    if 'receipt' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Read the image file
        image_bytes = file.read()
        
        # Process the receipt
        result = process_receipt(image_bytes)
        
        if result is None:
            return jsonify({"error": "Failed to process receipt"}), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 