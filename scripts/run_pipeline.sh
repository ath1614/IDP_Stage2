#!/bin/bash

# ==========================================
# APAR Automation Pipeline Runner
# ==========================================

# Navigate to project root (assuming script is in scripts/)
cd "$(dirname "$0")/.."

# Check if venv exists
if [ ! -d "venv_llm" ]; then
    echo "Error: venv_llm not found. Please run scripts/setup_local_separated.sh first."
    exit 1
fi

# Activate the environment
source venv_llm/bin/activate

# Check input argument
if [ -z "$1" ]; then
    echo "Usage: ./scripts/run_pipeline.sh <path_to_pdf>"
    echo "Example: ./scripts/run_pipeline.sh 'data/APAR 1.pdf'"
    exit 1
fi

INPUT_PDF="$1"

echo "=========================================="
echo "Starting APAR Processing Pipeline"
echo "Input File: $INPUT_PDF"
echo "=========================================="

# Run the python pipeline script
python src/process_pipeline.py "$INPUT_PDF"

echo "=========================================="
echo "Pipeline Finished."
echo "Check the 'output' directory for the generated DOCX file."
echo "=========================================="
