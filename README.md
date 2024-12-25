# Receiptify

A web platform that helps users compare prices across different stores by analyzing uploaded receipts. Users can upload photos of their receipts, which are then processed using OCR to extract item and price information. This data is used to create a searchable database of prices across different stores.

## Features

- Receipt photo upload and OCR processing
- User authentication and personal receipt history
- Price comparison across different stores
- User-friendly interface to view and compare prices
- Store-specific price tracking
- Product price history
- Real-time price updates and notifications

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Authentication & Database: Firebase
- OCR: EasyOCR
- Cloud Storage: Firebase Storage

## Setup

1. Install Python 3.8 or higher
2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up Firebase:

   - Create a new Firebase project at https://console.firebase.google.com
   - Enable Authentication (Email/Password)
   - Create a Cloud Firestore database
   - Enable Storage
   - Download your Firebase configuration
   - Create a `.env` file with your Firebase credentials

4. Run the development server:

```bash
python server/app.py
```

## Project Structure

- `/client` - Frontend files (HTML, CSS, JS)
  - `/js` - JavaScript files including Firebase integration
  - `/css` - Stylesheets
  - `/images` - Static images and icons
- `/server` - Python Flask backend
  - `/services` - Business logic and Firebase integration
  - `/routes` - API endpoints
- `/shared` - Shared utilities and types
- `/config` - Configuration files (Firebase, etc.)
