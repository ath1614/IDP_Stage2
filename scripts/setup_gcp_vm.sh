#!/bin/bash

# Exit on error
set -e

echo "==========================================="
echo "Setting up OCR Service on GCP VM (T4 GPU)"
echo "==========================================="

# 1. System Updates and Dependencies
echo "[1/5] Updating system and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git libgl1 libglib2.0-0 build-essential

# 2. Check for NVIDIA Drivers
echo "[2/5] Checking NVIDIA drivers..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA drivers not found. Installing..."
    # This is the standard way to install T4 drivers on GCP Debian/Ubuntu images
    curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
    sudo python3 install_gpu_driver.py
    rm install_gpu_driver.py
    echo "Drivers installed. You might need to reboot."
else
    echo "NVIDIA drivers already installed."
    nvidia-smi
fi

# 3. Create Virtual Environment
echo "[3/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# 4. Install Python Dependencies
echo "[4/5] Installing Python libraries..."
source venv/bin/activate
pip install --upgrade pip
# Install torch with CUDA support explicitly to be safe
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# 5. Setup Finished
echo "==========================================="
echo "Setup Complete!"
echo "To start the service:"
echo "  1. source venv/bin/activate"
echo "  2. python ocr_service.py"
echo "==========================================="
