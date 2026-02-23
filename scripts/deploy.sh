#!/bin/bash

# Load configuration from .env
ENV_FILE="$(dirname "$0")/../.env"
if [ -f "$ENV_FILE" ]; then
    # Use export to make variables available
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Configuration
VM_IP="${OCR_VM_IP:-34.47.176.38}"
USER="tech"
FILES="src/ocr_service.py requirements.txt scripts/setup_gcp_vm.sh"

echo "==========================================="
echo "Deploying to GCP VM: $USER@$VM_IP"
echo "==========================================="

# 1. Transfer Files
echo "[1/2] Transferring files..."
echo "You may be asked for your SSH password."
scp $FILES $USER@$VM_IP:~/

# 2. Run Setup Script Remotely
echo "[2/2] Running setup script on VM..."
echo "Connecting via SSH..."
ssh $USER@$VM_IP "chmod +x setup_gcp_vm.sh && ./setup_gcp_vm.sh"

echo "==========================================="
echo "Deployment Finished!"
echo "To check the service logs on the VM, run:"
echo "  ssh $USER@$VM_IP"
echo "  source venv/bin/activate"
echo "  python ocr_service.py"
echo "==========================================="
