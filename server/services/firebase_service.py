import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
import pyrebase
from datetime import datetime
import os
from config.firebase_config import FIREBASE_CONFIG, FIREBASE_ADMIN_CONFIG

class FirebaseService:
    def __init__(self):
        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_ADMIN_CONFIG)
            firebase_admin.initialize_app(cred, {
                'storageBucket': FIREBASE_CONFIG['storageBucket']
            })
        
        # Initialize Pyrebase for client operations
        self.pb = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.db = firestore.client()
        self.bucket = storage.bucket()
        
    def verify_token(self, id_token):
        """Verify Firebase ID token."""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token['uid']
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None
    
    async def save_receipt(self, user_id, receipt_data, image_file):
        """Save receipt data and image to Firebase."""
        try:
            # Upload image to Firebase Storage
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = f"receipts/{user_id}/{timestamp}.jpg"
            blob = self.bucket.blob(image_path)
            blob.upload_from_string(
                image_file.read(),
                content_type='image/jpeg'
            )
            
            # Get the public URL
            image_url = blob.public_url
            
            # Save receipt data to Firestore
            receipt_ref = self.db.collection('receipts').document()
            receipt_data.update({
                'user_id': user_id,
                'image_url': image_url,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'status': 'processed'
            })
            receipt_ref.set(receipt_data)
            
            return receipt_ref.id
            
        except Exception as e:
            print(f"Error saving receipt: {str(e)}")
            raise
    
    def get_user_receipts(self, user_id):
        """Get all receipts for a user."""
        try:
            receipts = []
            query = self.db.collection('receipts')\
                         .where('user_id', '==', user_id)\
                         .order_by('timestamp', direction=firestore.Query.DESCENDING)
            
            for doc in query.stream():
                receipt = doc.to_dict()
                receipt['id'] = doc.id
                receipts.append(receipt)
            
            return receipts
            
        except Exception as e:
            print(f"Error getting receipts: {str(e)}")
            raise
    
    def get_price_comparisons(self, item_name):
        """Get price comparisons for an item across different stores."""
        try:
            prices = []
            query = self.db.collection('receipts')\
                         .where('items.name', '==', item_name)\
                         .order_by('timestamp', direction=firestore.Query.DESCENDING)
            
            for doc in query.stream():
                receipt = doc.to_dict()
                for item in receipt['items']:
                    if item['name'] == item_name:
                        prices.append({
                            'store': receipt['store'],
                            'price': item['price'],
                            'date': receipt['timestamp']
                        })
            
            return prices
            
        except Exception as e:
            print(f"Error getting price comparisons: {str(e)}")
            raise

# Create a singleton instance
firebase_service = FirebaseService() 