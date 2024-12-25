from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import easyocr
from PIL import Image
import io
import re
from datetime import datetime
from services.firebase_service import firebase_service
from functools import wraps

app = Flask(__name__)
CORS(app)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "No authorization token provided"}), 401
        
        token = auth_header.split('Bearer ')[1]
        user_id = firebase_service.verify_token(token)
        
        if not user_id:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated_function

def process_receipt(image_bytes):
    """Process the receipt image and extract relevant information."""
    try:
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Perform OCR
        results = reader.readtext(image)
        
        # Extract text from results
        text_results = [result[1] for result in results]
        
        # Extract store name (assuming it's in the first few lines)
        store_name = text_results[0] if text_results else "Unknown Store"
        
        # Look for price patterns and item names
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
        
        return {
            "store": store_name,
            "date": datetime.now().isoformat(),
            "items": items
        }
    
    except Exception as e:
        print(f"Error processing receipt: {str(e)}")
        return None

@app.route('/api/upload', methods=['POST'])
@require_auth
async def upload_receipt(user_id):
    """Handle receipt upload and processing."""
    if 'receipt' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Process the receipt
        image_bytes = file.read()
        file.seek(0)  # Reset file pointer for later use
        
        result = process_receipt(image_bytes)
        if result is None:
            return jsonify({"error": "Failed to process receipt"}), 500
        
        # Save to Firebase
        receipt_id = await firebase_service.save_receipt(user_id, result, file)
        result['id'] = receipt_id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/receipts', methods=['GET'])
@require_auth
def get_receipts(user_id):
    """Get all receipts for the authenticated user."""
    try:
        receipts = firebase_service.get_user_receipts(user_id)
        return jsonify(receipts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare/<item_name>', methods=['GET'])
@require_auth
def compare_prices(user_id, item_name):
    """Compare prices for a specific item across different stores."""
    try:
        prices = firebase_service.get_price_comparisons(item_name)
        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 