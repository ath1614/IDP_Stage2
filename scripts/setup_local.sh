#!/bin/bash

# Exit on error
set -e

echo "==========================================="
echo "Setting up LOCAL Environment (macOS)"
echo "==========================================="

# 1. Clean up existing venv if it's broken
if [ -d "venv" ]; then
    echo "Removing broken virtual environment..."
    rm -rf venv
fi

# 2. Create new venv
echo "Creating new virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
echo "Installing dependencies..."
pip install --upgrade pip

# Install common libraries
pip install flask requests python-docx

# Install Surya OCR (This will pull compatible torch/opencv for Mac)
echo "Installing Surya OCR..."
pip install surya-ocr

# Install Transformers (needed for tokenizer/models)
pip install transformers

echo "==========================================="
echo "Local Setup Complete!"
echo "To run the OCR service:"
echo "  source venv/bin/activate"
echo "  python ocr_service.py"
echo "==========================================="
