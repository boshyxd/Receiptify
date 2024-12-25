# Receiptify

A web platform that helps users compare prices across different stores by analyzing uploaded receipts. Users can upload photos of their receipts, which are then processed using OCR to extract item and price information. This data is used to create a searchable database of prices across different stores.

## Features

- Receipt photo upload and OCR processing
- Price comparison across different stores
- User-friendly interface to view and compare prices
- Store-specific price tracking
- Product price history

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- OCR: Tesseract/EasyOCR
- Database: SQLite (initially)

## Setup

1. Install Python 3.8 or higher
2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Run the development server:

```bash
python server/app.py
```

## Project Structure

- `/client` - Frontend files (HTML, CSS, JS)
- `/server` - Python backend
- `/docs` - Documentation
- `/shared` - Shared utilities and types
