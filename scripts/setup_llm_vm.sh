#!/bin/bash

# Exit on error
set -e

echo "==========================================="
echo "Setting up LLM Service on GCP VM"
echo "==========================================="

# 1. System Updates and Dependencies
echo "[1/4] Updating system..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git build-essential

# 2. Check for NVIDIA Drivers
echo "[2/4] Checking NVIDIA drivers..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "Installing NVIDIA drivers..."
    curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
    sudo python3 install_gpu_driver.py
    rm install_gpu_driver.py
else
    echo "NVIDIA drivers already installed."
fi

# 3. Create Virtual Environment
echo "[3/4] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 4. Install vLLM and Dependencies
echo "[4/4] Installing vLLM (This may take a while)..."
source venv/bin/activate
pip install --upgrade pip

# CRITICAL FIX: The error "undefined symbol: cuTensorMapEncodeTiled" means vLLM was built for CUDA 12+
# but the system might have older drivers or incompatibilities.
# We will force install a version compatible with T4/standard GCP drivers (likely CUDA 11.8 or 12.1)
# and install numpy<2 to avoid other known issues.

pip install "numpy<2"
# Force reinstall torch with CUDA 12.1 to match vLLM's expectation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
# Install vLLM again (it should pick up the correct torch)
pip install vllm flask fastapi uvicorn

echo "==========================================="
echo "Setup Complete!"
echo "Make sure you have logged into HuggingFace if using gated models:"
echo "  huggingface-cli login"
echo ""
echo "To start the service:"
echo "  source venv/bin/activate"
echo "  python llm_service.py"
echo "==========================================="
