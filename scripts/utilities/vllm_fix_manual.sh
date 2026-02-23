#!/bin/bash

# Exit on error
set -e

echo "==========================================="
echo "MANUAL FIX: Installing CUDA 11.8 Compatible vLLM"
echo "==========================================="
echo "This fixes 'undefined symbol: cuTensorMapEncodeTiled' by using CUDA 11.8 builds"
echo "instead of the default CUDA 12 builds which require newer drivers."
echo "==========================================="

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found! Please run setup_llm_vm.sh first."
    exit 1
fi

echo "[1/4] Uninstalling conflicting packages..."
pip uninstall -y numpy torch torchvision torchaudio vllm xformers opencv-python opencv-python-headless flashinfer-python xgrammar

echo "[2/4] Installing dependencies..."
# 1. Install Numpy < 2
pip install "numpy<2"

# 2. Install OpenCV Headless compatible with Numpy < 2
pip install "opencv-python-headless<4.11"

# 3. Install PyTorch with CUDA 11.8 explicitly
echo "Installing PyTorch for CUDA 11.8..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 4. Install vLLM optimized for CUDA 11.8
# We use a specific wheel for Python 3.10 and CUDA 11.8
VLLM_VERSION=0.6.1.post1
PYTHON_VERSION=310
WHEEL_URL="https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl"

echo "Installing vLLM ${VLLM_VERSION} for CUDA 11.8..."
echo "Downloading wheel from: $WHEEL_URL"

# Install directly from the wheel
pip install "$WHEEL_URL" --extra-index-url https://download.pytorch.org/whl/cu118

# Install flask for the API
pip install flask

echo "[3/4] Verifying Installation..."
python3 -c "import torch; print(f'Torch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"

echo "==========================================="
echo "Fix Complete! Try running the service now:"
echo "  source venv/bin/activate"
echo "  python llm_service.py"
echo "==========================================="
