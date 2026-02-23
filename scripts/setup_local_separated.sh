#!/bin/bash
set -e

echo "Setting up OCR environment (venv_ocr)..."
python3 -m venv venv_ocr
source venv_ocr/bin/activate
pip install -r requirements_ocr.txt
deactivate

echo "Setting up LLM/Client environment (venv_llm)..."
python3 -m venv venv_llm
source venv_llm/bin/activate
pip install -r requirements_llm.txt
deactivate

echo "Setup complete. To run the pipeline:"
echo "source venv_llm/bin/activate"
echo "python process_pipeline.py <pdf_file>"
