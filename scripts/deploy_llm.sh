#!/bin/bash

# Load configuration from .env
ENV_FILE="$(dirname "$0")/../.env"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Configuration
LLM_VM_IP="${LLM_VM_IP:-34.93.108.135}"
USER="tech" # Assuming same user
 FILES="src/llm_service.py scripts/setup_llm_vm.sh"
 
 echo "==========================================="
 echo "Deploying LLM Service to: $LLM_VM_IP"
 echo "==========================================="

scp $FILES $USER@$LLM_VM_IP:~/

echo "Running setup on VM..."
ssh $USER@$LLM_VM_IP "chmod +x setup_llm_vm.sh && ./setup_llm_vm.sh"

echo "Deployment Done!"
