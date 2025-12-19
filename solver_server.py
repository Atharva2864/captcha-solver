#!/usr/bin/env python3
"""
Captcha Solver - A lightweight HTTP server for solving image CAPTCHAs
using Tesseract OCR with advanced image preprocessing.

Author: Amey
License: MIT
"""

import base64
import re
from collections import Counter

import cv2
import numpy as np
import pytesseract
from flask import Flask, request, jsonify

app = Flask(__name__)


def preprocess_image(img_bytes: bytes) -> np.ndarray | None:
    """
    Preprocess CAPTCHA image for better OCR accuracy.
    
    Applies multiple image processing techniques:
    - Grayscale conversion
    - CLAHE (Contrast Limited Adaptive Histogram Equalization)
    - Adaptive thresholding
    - Morphological operations
    - Image scaling
    
    Args:
        img_bytes: Raw image bytes
        
    Returns:
        Preprocessed image as numpy array, or None if processing fails
    """
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    
    # Adaptive threshold to handle varying backgrounds
    thresh = cv2.adaptiveThreshold(
        contrast, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 2
    )
    
    # Clean up noise with morphological operations
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Invert if background is dark
    if np.mean(cleaned) < 127:
        cleaned = cv2.bitwise_not(cleaned)
    
    # Scale up for better OCR accuracy
    scaled = cv2.resize(cleaned, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    return scaled


def solve_captcha(img_bytes: bytes) -> str | None:
    """
    Solve CAPTCHA using multiple OCR strategies.
    
    Tries multiple Tesseract configurations and preprocessing approaches,
    then returns the most common result for better accuracy.
    
    Args:
        img_bytes: Raw CAPTCHA image bytes
        
    Returns:
        Solved CAPTCHA text, or None if solving fails
    """
    results = []
    
    # Strategy 1: Advanced preprocessing with multiple PSM modes
    try:
        processed = preprocess_image(img_bytes)
        if processed is not None:
            configs = [
                '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                '--psm 8 --oem 3',
                '--psm 6 --oem 3',
            ]
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed, config=config)
                    text = re.sub(r'[^a-zA-Z0-9]', '', text.strip())
                    if text and len(text) >= 4:
                        results.append(text)
                except Exception:
                    pass
    except Exception as e:
        print(f"Preprocessing error: {e}")
    
    # Strategy 2: Simple threshold approach
    try:
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            _, simple_thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            simple_scaled = cv2.resize(simple_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text = pytesseract.image_to_string(simple_scaled, config='--psm 7 --oem 3')
            text = re.sub(r'[^a-zA-Z0-9]', '', text.strip())
            if text and len(text) >= 4:
                results.append(text)
    except Exception:
        pass
    
    if not results:
        return None
    
    # Return most common result (voting mechanism)
    counter = Counter(results)
    return counter.most_common(1)[0][0]


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "captcha-solver",
        "version": "1.0.0"
    })


@app.route('/solve', methods=['POST'])
def solve():
    """
    Solve CAPTCHA endpoint.
    
    Expects JSON payload with 'image' field containing base64-encoded image.
    Supports both raw base64 and data URL format.
    
    Returns:
        JSON with 'success' boolean and either 'text' (solved) or 'error' (failed)
    """
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                "success": False, 
                "error": "No image provided. Send JSON with 'image' field."
            }), 400
        
        image_data = data['image']
        
        # Handle data URL format (e.g., "data:image/png;base64,...")
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        img_bytes = base64.b64decode(image_data)
        
        # Solve CAPTCHA
        result = solve_captcha(img_bytes)
        
        if result:
            print(f"✓ Solved: {result}")
            return jsonify({"success": True, "text": result})
        else:
            print("✗ Could not solve")
            return jsonify({"success": False, "error": "Could not solve CAPTCHA"})
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API documentation."""
    return jsonify({
        "name": "Captcha Solver",
        "version": "1.0.0",
        "description": "A free, self-hosted CAPTCHA solver using Tesseract OCR",
        "endpoints": {
            "GET /": "This documentation",
            "GET /health": "Health check",
            "POST /solve": "Solve CAPTCHA (send JSON with base64 'image')"
        },
        "example": {
            "curl": "curl -X POST http://localhost:5555/solve -H 'Content-Type: application/json' -d '{\"image\": \"<base64_image>\"}'"
        }
    })


def main():
    """Start the CAPTCHA solver server."""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║           Captcha Solver Server v1.0.0                ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Endpoints:                                           ║
    ║    GET  /        - API documentation                  ║
    ║    GET  /health  - Health check                       ║
    ║    POST /solve   - Solve CAPTCHA                      ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Server running at: http://127.0.0.1:5555             ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    app.run(host='127.0.0.1', port=5555, debug=False)


if __name__ == '__main__':
    main()
