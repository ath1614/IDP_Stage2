#!/bin/bash

# 1. Setup OCR Environment (venv_ocr)
echo "========================================"
echo "Setting up OCR Environment (venv_ocr)..."
echo "========================================"

if [ -d "venv_ocr" ]; then
    echo "Removing existing venv_ocr..."
    rm -rf venv_ocr
fi

python3 -m venv venv_ocr
source venv_ocr/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies from requirements_ocr.txt
# We use the exact versions from the VM for critical packages
echo "Installing OCR dependencies..."
pip install -r requirements_ocr.txt

echo "OCR Environment setup complete."
deactivate

# 2. Setup LLM Environment (venv_llm)
echo "========================================"
echo "Setting up LLM Environment (venv_llm)..."
echo "========================================"

if [ -d "venv_llm" ]; then
    echo "Removing existing venv_llm..."
    rm -rf venv_llm
fi

python3 -m venv venv_llm
source venv_llm/bin/activate

pip install --upgrade pip

# Install basic LLM deps (vllm might not work on Mac easily, but we install basics)
# The user mostly runs LLM on VM, but requested separate venv.
pip install flask requests

echo "LLM Environment setup complete."
deactivate

echo "========================================"
echo "All environments set up successfully."
echo "To run OCR locally: ./run_local_ocr.sh"
echo "========================================"
